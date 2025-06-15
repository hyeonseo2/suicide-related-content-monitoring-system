#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 블로그 API 크롤러
"""

import urllib.request
import urllib.parse
import json
from .base_crawler import BaseCrawler


class NaverCrawler(BaseCrawler):
    """네이버 블로그 API 크롤러"""

    def __init__(self, config):
        """네이버 크롤러 초기화"""
        super().__init__(config)
        self.platform_name = "Naver Blog"

    def search(self, keyword, max_results=None):
        """네이버 블로그 검색 - 수집량 매개변수 추가"""
        if not self.config.has_naver_config():
            print("네이버 API 설정이 없습니다. 네이버 블로그 검색을 건너뜁니다.")
            return []

        # 기본값 설정 및 API 제한 확인
        if max_results is None:
            max_results = self.config.max_results_per_platform

        # 네이버 API는 한 번에 최대 100개까지만 요청 가능
        display_count = min(max_results, 100)

        try:
            print(f"네이버 블로그 API 검색 시작 - 키워드: {keyword}, 요청량: {display_count}개")

            # API 요청
            enc_text = urllib.parse.quote(keyword)
            url = f"https://openapi.naver.com/v1/search/blog.json?query={enc_text}&display={display_count}&sort=date"

            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.config.naver_client_id)
            request.add_header("X-Naver-Client-Secret", self.config.naver_client_secret)

            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))

            print(f"API 응답 - 전체 결과: {data.get('total', 0)}개, 반환: {len(data.get('items', []))}개")

            # 결과 처리
            results = []
            for item in data['items']:
                data_item = self._create_data_item(
                    url=item['link'],
                    title=item['title'],
                    content=item['description'],
                    keyword=keyword,
                    created_at=item['postdate']
                )
                data_item['bloggername'] = item.get('bloggername', '')
                data_item['bloggerlink'] = item.get('bloggerlink', '')
                results.append(data_item)

            print(f"네이버 블로그에서 {len(results)}개 게시글 수집 완료")
            return results

        except Exception as e:
            print(f"네이버 블로그 검색 중 오류 발생: {e}")
            return []
