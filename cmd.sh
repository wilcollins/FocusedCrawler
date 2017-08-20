#!/bin/bash
python FocusedCrawler.py \
  --seeds "trump" \
  --blacklist_domains "www.breitbart.com" \
  --relevancy_threshold 0.8 \
  --irrelevancy_threshold 0.7 \
  --page_limit 15 \
  --link_limit 30 \
  --adaptive true \
  --relevant_urls="www.cnn.com" \
  --irrelevant_urls="www.foxnews.com"
