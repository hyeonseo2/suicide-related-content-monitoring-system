#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
디시인사이드 크롤러
"""

import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
from .base_crawler import BaseCrawler


class DCInsideCrawler(BaseCrawler):
    """디시인사이드 크롤러"""

    def __init__(self, config):
        """디시인사이드 크롤러 초기화"""
        super().__init__(config)
        self.platform_name = "DCInside"
        self._setup_session()

    def _setup_session(self):
        """HTTP 세션 설정"""
        self.session = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        self.session.headers.update(headers)

    def search(self, keyword, max_results=None):
        if max_results is None:
            max_results = 30

        try:
            print(f"디시인사이드 검색 시작 - 키워드: {keyword}, 목표: {max_results}개")
            results = []
            page = 1

            while len(results) < max_results:
                search_url = f"https://search.dcinside.com/combine/q/{urllib.parse.quote(keyword)}/p/{page}"
                response = self.session.get(search_url, timeout=self.config.timeout)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                links = self._extract_links(soup)
                if not links:
                    break  # 더 이상 결과 없음

                for link in links:
                    if len(results) >= max_results:
                        break
                    post_url, post_title = self._process_link(link)
                    if not post_url:
                        continue
                    content = self._crawl_post_content(post_url)
                    data_item = self._create_data_item(
                        url=post_url,
                        title=post_title,
                        content=content,
                        keyword=keyword,
                        created_at=datetime.now().strftime("%Y-%m-%d")
                    )
                    results.append(data_item)
                    self._delay_request()

                page += 1  # 다음 페이지로

            successful_crawls = len([d for d in results if d['crawl_success']])
            success_rate = (successful_crawls / len(results) * 100) if results else 0

            print(f"디시인사이드에서 {len(results)}개 게시글 수집 완료")
            print(f"크롤링 성공률: {success_rate:.1f}% ({successful_crawls}/{len(results)})")
            return results

        except Exception as e:
            print(f"디시인사이드 검색 중 오류: {e}")
            return []

    def _extract_links(self, soup):
        """링크 추출"""
        links = soup.find_all('a', class_='tit')

        if not links:
            # 대안 선택자들
            alternative_selectors = [
                'a[href*="/board/view/"]',
                '.gall_tit a',
                '.title a',
                'a.title',
                '.ub-word a'
            ]

            for selector in alternative_selectors:
                try:
                    links = soup.select(selector)
                    if links:
                        print(f"대안 선택자 '{selector}'로 {len(links)}개 링크 발견")
                        break
                except Exception:
                    continue

        return links

    def _process_link(self, link):
        """링크 처리"""
        href = link.get('href', '')

        if href.startswith('/'):
            post_url = 'https://gall.dcinside.com' + href
        elif href.startswith('http'):
            post_url = href
        else:
            return None, None

        post_title = link.text.strip()
        return post_url, post_title

    def _crawl_post_content(self, url):
        """게시글 내용 크롤링"""
        try:
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # 다양한 선택자로 내용 추출 시도
            content_selectors = [
                'div.writing_view_box',
                '.write_div',
                '.view_content_wrap',
                '.gallery_re_cont',
                '.dccon_wrapper',
                '.writing_view_box .inner',
                '.view_content',
                '.usertxt'
            ]

            for selector in content_selectors:
                try:
                    content_div = soup.select_one(selector)
                    if content_div:
                        extracted_text = content_div.get_text(strip=True)
                        if extracted_text and len(extracted_text) > 10:
                            return extracted_text
                except Exception:
                    continue

            return ""

        except Exception:
            return ""

    def close(self):
        """세션 정리"""
        if hasattr(self, 'session'):
            self.session.close()
