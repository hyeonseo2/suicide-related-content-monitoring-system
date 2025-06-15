#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 블로그 API 크롤러
"""

import urllib.request
import urllib.parse
import json
import time
from .base_crawler import BaseCrawler


class NaverCrawler(BaseCrawler):
    """네이버 블로그 API 크롤러"""

    def __init__(self, config):
        """네이버 크롤러 초기화"""
        super().__init__(config)
        self.platform_name = "Naver Blog"
        self.max_api_results = 1000  # API 최대 수집 가능 개수

    def search(self, keyword, max_results=None):
        """네이버 블로그 검색 - 전체 검색 결과 건수 표시 추가"""
        if not self.config.has_naver_config():
            print("네이버 API 설정이 없습니다. 네이버 블로그 검색을 건너뜁니다.")
            return []

        # API 제약 조건 적용
        user_request = max_results or self.config.max_results_per_platform
        max_results = max(1, min(user_request, self.max_api_results))

        collected_items = []
        start_position = 1
        remaining = max_results
        total_results = 0  # 전체 검색 결과 건수 저장 변수

        try:
            print(f"\n[Naver Blog] 검색 시작 - 키워드: '{keyword}'")

            while remaining > 0 and start_position <= self.max_api_results:
                display_count = min(remaining, 100, self.max_api_results - start_position + 1)
                enc_text = urllib.parse.quote(keyword)
                url = f"https://openapi.naver.com/v1/search/blog.json?query={enc_text}&display={display_count}&start={start_position}&sort=date"

                # API 요청
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", self.config.naver_client_id)
                request.add_header("X-Naver-Client-Secret", self.config.naver_client_secret)

                response = urllib.request.urlopen(request)
                data = json.loads(response.read().decode('utf-8'))
                items = data.get('items', [])

                # 전체 검색 결과 건수 추출 (첫 번째 응답에서만)
                if total_results == 0:
                    total_results = data.get('total', 0)
                    print(f"※ 전체 검색 결과: {total_results:,}건")
                    print(f"※ API 최대 수집 가능량: {self.max_api_results}건")

                # 결과 처리
                for item in items:
                    data_item = self._create_data_item(
                        url=item['link'],
                        title=item['title'],
                        content=item['description'],
                        keyword=keyword,
                        created_at=item['postdate']
                    )
                    data_item['bloggername'] = item.get('bloggername', '')
                    data_item['bloggerlink'] = item.get('bloggerlink', '')
                    collected_items.append(data_item)

                # 다음 페이지 설정
                remaining -= len(items)
                start_position += display_count

                # 더 이상 데이터 없으면 중단
                if len(items) < display_count:
                    break

                # API 호출 간격 유지 (초당 10회 이하)
                time.sleep(0.1)

            actual_collected = len(collected_items)
            print(f"\n[Naver Blog] 수집 완료")
            print(f"- 목표 수집량: {max_results}건")
            print(f"- 실제 수집량: {actual_collected}건")
            print(f"- 전체 검색 결과: {total_results:,}건")

            if user_request > actual_collected:
                print(f"※ 주의: 요청량({user_request}개) 중 {actual_collected}개만 수집 가능했습니다.")

            return collected_items

        except Exception as e:
            print(f"\n[Naver Blog] 검색 중 오류 발생: {e}")
            print(f"- 현재까지 수집된 결과: {len(collected_items)}건")
            print(f"- 전체 검색 결과: {total_results:,}건")
            return collected_items
