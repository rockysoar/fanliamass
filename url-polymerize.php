<?php
/**
 * Author: 君升 junhua.zhang@fanli.com
 * Created Time: Fri 16 Dec 2016 09:31:16 AM CST
 */
$counter = 0;
$handler = fopen('/usr/local/workdata/exchange/kafka-path.csv', 'r');
if (!$handler) exit('file not exists');

while ($row = fgets($handler)) {
    if (empty($row)) continue;
    $counter++;

    $path = trim($row, "\r\n'\"/ ");
    if (preg_match('/\.(js|css|html|png|jpg)/', $path)) continue;

    $info = parse_url($path);
    $host = $info['host'];
    $path = $info['path'];
    $query = isset($info['query']) ? $info['query'] : '';

    $keys = $keys_ = [];
    $keys = preg_split('/\/|-/', $path, 10, PREG_SPLIT_NO_EMPTY);
    for ($i = 0; $i < count($keys); $i++) {
        $key = $keys[$i]; $value = $keys[$i+1];
        if (dropPair($key, $value)) {
            $i++; continue;
        }
        if (dropItem($key)) continue;
        $keys_[] = $key;
    }

    $keys = null;
    parse_str($query, $keys);
    foreach($keys as $key=>$value) {
        if (empty($value)) continue;
        if (dropPair($key, $value) || dropItem($key)) continue;
        $keys_[] = $key;
    }

    if (count($keys_) > 4) {
        $keys_ = array_slice($keys_, 0, 4);
    }
    if (empty($keys_)) continue;

    $urlCode = strtolower(implode('.', $keys_));
    $urlCodes[$urlCode]++;
}

function dropPair($key, $value) {
    $drop = false;
    $drop = $drop || !is_string($value);
    $drop = $drop || preg_match('/^[\w-\.~=]{31,}$/', $value);
    $drop = $drop || in_array($key, ['jsoncallback','spm','lc','_t','__','_']);
    $drop = $drop || (in_array($key, ['size','page','page_size','pagesize','psize']) && is_numeric($value));
    $drop = $drop || ('size' == $key && in_array($value, ['big', 'small']));
    $drop = $drop || ('sort' == $key && in_array($value, ['asort-desc', 'asort-asc']));
    $drop = $drop || ('app_ref' == $key && (empty($value) || preg_match('/^\w{12,}/', $value)));
    $drop = $drop || ('deviceno' == $key && (empty($value) || preg_match('/^\w{12,}/', $value)));
    $drop = $drop || ('devid' == $key && (empty($value) ||  preg_match('/^\w{12,}/', $value)));
    $drop = $drop || ('msg' == $key && (empty($value) || preg_match('/^\w{12,}/', $value)));
    $drop = $drop || ('security_id' == $key && (empty($value) || preg_match('/^\w{12,}/', $value)));

    // 字母数字混合混乱度 16进制字符串数字出现频率为0.625(+-0.05)
    if (strlen($key) > 10 && false === strpos($key, '_')) {
        $numCount = 0;
        foreach(str_split($key) as $char) {
            // 数字数量
            if (ord($char) >= 48 && ord($char) <= 57) $numCount++;
        }
        $numRate = $numCount/strlen($key);
        $drop = $drop || ($numRate >= .575 && $numRate <= .675);
    }

    // 数字被字母分割为至少3段(熵高)
    $m = null;
    preg_match_all('/(\d+)/', $key, $m);
    $drop = $drop || (isset($m[1]) && count($m[1]) >= 3);

    return $drop;
}

// key由数字字母下划线组成, 以非数字打头，长度不超过32, 字母数字混合混乱度不高
function dropItem($key) {
    $drop = false;
    $drop = $drop || empty($key);
    $drop = $drop || is_numeric($key);
    $drop = $drop || !preg_match('/^[a-zA-Z_]\w*$/', $key);
    $drop = $drop || preg_match('/^\w{32,}$/', $key);

    return $drop;
}

print_r($urlCodes);
echo count($urlCodes), '; ', $counter;

