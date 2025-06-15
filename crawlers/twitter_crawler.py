#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter API 크롤러
"""

import tweepy
import pytz
from datetime import datetime, timedelta
from .base_crawler import BaseCrawler


class TwitterCrawler(BaseCrawler):
    """Twitter API 크롤러"""

    def __init__(self, config):
        """Twitter 크롤러 초기화"""
        super().__init__(config)
        self.platform_name = "Twitter"

        if config.has_twitter_config():
            self.client = tweepy.Client(
                bearer_token=config.twitter_bearer_token,
                wait_on_rate_limit=True
            )
        else:
            self.client = None

    def search(self, keyword, start_date=None, end_date=None, max_results=None):
        """Twitter 검색 - 수집량 매개변수 추가"""
        if not self.client:
            print("Twitter API 설정이 없습니다. Twitter 검색을 건너뜁니다.")
            return []

        # 기본값 설정
        if max_results is None:
            max_results = self.config.max_results_per_platform

        try:
            # 안전한 시간 계산
            end_time = self._get_safe_end_time(end_date)
            start_time = start_date.strftime("%Y-%m-%dT00:00:00Z") if start_date else None

            # 검색 실행
            query = f"{keyword} -is:retweet lang:ko"
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                start_time=start_time,
                end_time=end_time,
                tweet_fields=['created_at', 'author_id'],
                max_results=10
            ).flatten(limit=max_results)

            # 결과 처리
            results = []
            for tweet in tweets:
                item = self._create_data_item(
                    url=f"https://twitter.com/user/status/{tweet.id}",
                    title="",
                    content=tweet.text,
                    keyword=keyword,
                    created_at=tweet.created_at
                )
                results.append(item)

            print(f"Twitter에서 {len(results)}개 게시글 수집 완료")
            return results

        except Exception as e:
            print(f"Twitter 검색 중 오류: {str(e)}")
            return []

    def _get_safe_end_time(self, end_date):
        """API 안전한 종료 시간 계산"""
        now_utc = datetime.now(pytz.UTC)
        safe_end_time = now_utc - timedelta(seconds=60)

        if end_date:
            user_end_time = end_date.replace(hour=23, minute=59, second=0)
            if user_end_time.tzinfo is None:
                user_end_time = pytz.UTC.localize(user_end_time)
            return min(user_end_time, safe_end_time).strftime("%Y-%m-%dT%H:%M:%SZ")

        return safe_end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
