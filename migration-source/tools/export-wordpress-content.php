<?php
/**
 * Sanitized WordPress content export for bloecher.de -> Hugo migration.
 *
 * CLI only.
 *
 * Usage:
 *   php export-wordpress-content.php /absolute/path/to/wordpress [output.json]
 *
 * The script loads the existing WordPress installation and exports only
 * migration-relevant public content. It never prints wp-config.php or DB credentials.
 */

if (!isset($argv) || !is_array($argv)) {
    fwrite(fopen('php://stderr', 'w'), "Command-line arguments unavailable.\n");
    exit(1);
}

$wpRoot = $argv[1] ?? null;
$output = $argv[2] ?? (__DIR__ . '/../export/wordpress-content.json');

if (!$wpRoot) {
    fwrite(fopen('php://stderr', 'w'), "Usage: php export-wordpress-content.php /path/to/wordpress [output.json]\n");
    exit(2);
}

$wpLoad = rtrim($wpRoot, '/\\') . '/wp-load.php';
if (!is_file($wpLoad)) {
    fwrite(fopen('php://stderr', 'w'), "wp-load.php not found: {$wpLoad}\n");
    exit(3);
}

define('WP_USE_THEMES', false);
require_once $wpLoad;

if (!function_exists('get_posts')) {
    fwrite(fopen('php://stderr', 'w'), "WordPress did not load correctly.\n");
    exit(4);
}

function clean_scalar($value) {
    if (is_string($value)) {
        return trim($value);
    }
    return $value;
}

function selected_meta($postId) {
    $keys = [
        '_wp_page_template',
        '_yoast_wpseo_title',
        '_yoast_wpseo_metadesc',
        '_yoast_wpseo_focuskw',
        '_yoast_wpseo_canonical',
        '_thumbnail_id',
    ];

    $out = [];
    foreach ($keys as $key) {
        $value = get_post_meta($postId, $key, true);
        if ($value !== '' && $value !== null) {
            $out[$key] = clean_scalar($value);
        }
    }
    return $out;
}

function post_language($postId) {
    if (function_exists('pll_get_post_language')) {
        $lang = pll_get_post_language($postId, 'slug');
        return $lang ?: null;
    }

    $terms = wp_get_post_terms($postId, 'language', ['fields' => 'slugs']);
    if (!is_wp_error($terms) && !empty($terms)) {
        return $terms[0];
    }

    return null;
}

function post_translations($postId) {
    if (function_exists('pll_get_post_translations')) {
        $translations = pll_get_post_translations($postId);
        if (is_array($translations)) {
            ksort($translations);
            return $translations;
        }
    }
    return [];
}

function attachment_info($attachmentId) {
    $attachmentId = (int) $attachmentId;
    if (!$attachmentId) {
        return null;
    }

    $path = get_attached_file($attachmentId);
    $meta = wp_get_attachment_metadata($attachmentId);

    return [
        'id' => $attachmentId,
        'title' => get_the_title($attachmentId),
        'url' => wp_get_attachment_url($attachmentId),
        'relative_upload_path' => $path ? _wp_relative_upload_path($path) : null,
        'alt' => get_post_meta($attachmentId, '_wp_attachment_image_alt', true),
        'caption' => wp_get_attachment_caption($attachmentId),
        'mime_type' => get_post_mime_type($attachmentId),
        'width' => is_array($meta) ? ($meta['width'] ?? null) : null,
        'height' => is_array($meta) ? ($meta['height'] ?? null) : null,
    ];
}

global $wpdb;

$postIds = $wpdb->get_col(
    "SELECT ID
     FROM {$wpdb->posts}
     WHERE post_type = 'page'
       AND post_status = 'publish'
     ORDER BY menu_order ASC, post_title ASC"
);

$posts = [];
foreach ($postIds as $postId) {
    $post = get_post((int) $postId);
    if ($post instanceof WP_Post) {
        $posts[] = $post;
    }
}

$exportPosts = [];
$attachmentIds = [];

foreach ($posts as $post) {
    $meta = selected_meta($post->ID);

    if (!empty($meta['_thumbnail_id'])) {
        $attachmentIds[(int) $meta['_thumbnail_id']] = true;
    }

    // Collect attachment IDs referenced through standard gallery/image shortcodes.
    if (preg_match_all('/(?:ids|id)=["\']?([0-9,]+)/i', $post->post_content, $matches)) {
        foreach ($matches[1] as $chunk) {
            foreach (explode(',', $chunk) as $id) {
                if (ctype_digit(trim($id))) {
                    $attachmentIds[(int) trim($id)] = true;
                }
            }
        }
    }

    $exportPosts[] = [
        'id' => (int) $post->ID,
        'parent_id' => (int) $post->post_parent,
        'menu_order' => (int) $post->menu_order,
        'post_type' => $post->post_type,
        'status' => $post->post_status,
        'title' => html_entity_decode(get_the_title($post), ENT_QUOTES | ENT_HTML5, 'UTF-8'),
        'slug' => $post->post_name,
        'url' => get_permalink($post),
        'date' => get_post_time(DATE_ATOM, true, $post),
        'modified' => get_post_modified_time(DATE_ATOM, true, $post),
        'excerpt_raw' => $post->post_excerpt,
        'content_raw' => $post->post_content,
        'language' => post_language($post->ID),
        'translations' => post_translations($post->ID),
        'meta' => $meta,
    ];
}

$attachments = [];
foreach (array_keys($attachmentIds) as $attachmentId) {
    $info = attachment_info($attachmentId);
    if ($info) {
        $attachments[] = $info;
    }
}

usort($attachments, fn($a, $b) => ($a['relative_upload_path'] ?? '') <=> ($b['relative_upload_path'] ?? ''));

$languages = [];
if (function_exists('pll_languages_list')) {
    foreach (pll_languages_list(['fields' => 'slug']) as $slug) {
        $languages[] = $slug;
    }
} else {
    $terms = get_terms([
        'taxonomy' => 'language',
        'hide_empty' => false,
        'fields' => 'slugs',
    ]);
    if (!is_wp_error($terms)) {
        $languages = array_values($terms);
    }
}

$data = [
    'schema_version' => 1,
    'generated_at' => gmdate(DATE_ATOM),
    'source' => [
        'site_url' => get_site_url(),
        'home_url' => get_home_url(),
        'wordpress_version' => get_bloginfo('version'),
    ],
    'languages' => $languages,
    'counts' => [
        'pages' => count($exportPosts),
        'referenced_attachments' => count($attachments),
    ],
    'pages' => $exportPosts,
    'attachments' => $attachments,
];

$dir = dirname($output);
if (!is_dir($dir) && !mkdir($dir, 0775, true) && !is_dir($dir)) {
    fwrite(fopen('php://stderr', 'w'), "Cannot create output directory: {$dir}\n");
    exit(5);
}

$json = json_encode(
    $data,
    JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
);

if ($json === false) {
    fwrite(fopen('php://stderr', 'w'), "JSON encoding failed: " . json_last_error_msg() . "\n");
    exit(6);
}

if (file_put_contents($output, $json . PHP_EOL) === false) {
    fwrite(fopen('php://stderr', 'w'), "Cannot write output: {$output}\n");
    exit(7);
}

fwrite(fopen('php://stdout', 'w'), "[OK] Exported " . count($exportPosts) . " published pages to {$output}\n");
fwrite(fopen('php://stdout', 'w'), "[OK] Languages: " . implode(', ', $languages) . "\n");
fwrite(fopen('php://stdout', 'w'), "[OK] Referenced attachments: " . count($attachments) . "\n");
