#!/usr/bin/php
<?php
// scrape recent plugins and theme vulnerabilities from wpvuldb.com
$page = file_get_contents('https://wpvulndb.com/');
$search = preg_match_all("/(?<=\"\>)(.*[0-9])(?=<\/a>)/", $page, $matches);
$vulnIDs = array_unique($matches[0]);
print "Execute the following commands to install vulnerable themes and plugins:\n\n";
foreach($vulnIDs as $ID){
	$vulnPage = file_get_contents("https://wpvulndb.com/vulnerabilities/$ID");
	$vulnType = preg_match("/(?<=affects-link\"\>\<a\shref\=\").*(?=\"\>)/", $vulnPage, $matchedType);
	$vulnVersion = preg_match("/(?<=\&lt\;\=\s).*(?=\s-)/", $vulnPage, $matchedVersion);
	if(strpos($matchedType[0], "theme") != false and $vulnVersion != false){
		shell_exec("wp --allow-root --path=/var/www/html theme install " . substr($matchedType[0], 8) . " --version=" . $matchedVersion[0]);
	} elseif(strpos($matchedType[0], "plugin") != false and $vulnVersion != false) {
		shell_exec("wp --allow-root --path=/var/www/html plugin install " . substr($matchedType[0], 9) . " --version=" . $matchedVersion[0]);
	}
}
shell_exec("chown -R www-data. /var/www/html/wp-content");
