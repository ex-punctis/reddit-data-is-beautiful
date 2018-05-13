# reddit-data-is-beautiful
Analysis of reddit's "dataisbeautiful" community

https://have-data-will-analyze.github.io/2018/04/29/Reddit-dataisbeautiful.html

## Python 2.7 scripts

The first script downloads html pages that contain lists of new posts. The second script extracts individual post urls from the saved lists. The third scrip uses post urls to download each post. Finally, the forth script parses individual post files and saves results into a tab delimited file.

Create a folder where you want to save your data, and edit the root_dir variable in each script to provide the path of this folder. Save user_agents_non_mobile.txt into this folder.

## R script

This script imports the tab delimited file created by the last python script, cleans up the data and creates plots.
