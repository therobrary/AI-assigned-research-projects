"""
title: Hello World Tool
author: OpenWebUI Community
author_url: https://github.com/open-webui/open-webui
version: 1.0.0
license: MIT
"""

from typing import Callable, Any

class Tools:
    def __init__(self):
        self.name = "hello_world"
        self.description = "A simple greeting tool that demonstrates basic OpenWebUI tool functionality"

    def greet(
        self,
        name: str = "World",
        language: str = "en",
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Generate a greeting message in different languages.
        
        :param name: Name to greet (default: "World")
        :param language: Language code (en, es, fr, de) (default: "en")
        :return: Greeting message
        """
        greetings = {
            "en": f"Hello, {name}!",
            "es": f"¡Hola, {name}!",
            "fr": f"Bonjour, {name}!",
            "de": f"Hallo, {name}!",
            "it": f"Ciao, {name}!",
            "pt": f"Olá, {name}!",
            "ru": f"Привет, {name}!",
            "ja": f"こんにちは, {name}!",
            "zh": f"你好, {name}!",
        }
        
        greeting = greetings.get(language.lower(), greetings["en"])
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Generated greeting for {name} in {language}", "done": True},
            })
        
        return greeting

    def get_supported_languages(
        self,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get list of supported languages for greetings.
        
        :return: List of supported language codes and names
        """
        languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French", 
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "zh": "Chinese",
        }
        
        result = "Supported languages:\n"
        for code, name in languages.items():
            result += f"- {code}: {name}\n"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": "Retrieved supported languages", "done": True},
            })
        
        return result.strip()

    def farewell(
        self,
        name: str = "friend",
        language: str = "en",
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Generate a farewell message in different languages.
        
        :param name: Name to say goodbye to (default: "friend")
        :param language: Language code (en, es, fr, de) (default: "en")
        :return: Farewell message
        """
        farewells = {
            "en": f"Goodbye, {name}!",
            "es": f"¡Adiós, {name}!",
            "fr": f"Au revoir, {name}!",
            "de": f"Auf Wiedersehen, {name}!",
            "it": f"Arrivederci, {name}!",
            "pt": f"Tchau, {name}!",
            "ru": f"До свидания, {name}!",
            "ja": f"さようなら, {name}!",
            "zh": f"再见, {name}!",
        }
        
        farewell = farewells.get(language.lower(), farewells["en"])
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Generated farewell for {name} in {language}", "done": True},
            })
        
        return farewell