#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기본 크롤러 추상 클래스
"""

from abc import ABC, abstractmethod
import time


class BaseCrawler(ABC):
    """모든 크롤러의 기본 클래스"""

    def __init__(self, config):
        """기본 크롤러 초기화"""
        self.config = config
        self.platform_name = "Unknown"

    @abstractmethod
    def search(self, keyword, start_date=None, end_date=None):
        """검색 메서드 - 하위 클래스에서 구현 필요"""
        pass

    def _clean_text(self, text):
        """텍스트 정리 공통 메서드"""
        if not text:
            return ""

        # HTML 태그 제거
        import re
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _delay_request(self):
        """요청 간격 조절"""
        time.sleep(self.config.request_delay)

    def _create_data_item(self, url, title, content, keyword, created_at=None):
        """표준 데이터 아이템 생성"""
        return {
            'platform': self.platform_name,
            'url': url,
            'title': self._clean_text(title),
            'content': self._clean_text(content)[:self.config.content_max_length],
            'keyword': keyword,
            'created_at': created_at,
            'crawl_success': len(content.strip()) > 0
        }
