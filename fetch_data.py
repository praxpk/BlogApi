import threading
import requests
from threading import Lock
from blog_api_logging import BlogApiLog
from functools import lru_cache, wraps
from datetime import datetime, timedelta

logger = BlogApiLog("fetch_data.py", "blog_api.log")
logger = logger.get_logger()


def timed_lru_cache(max_size, time_limit):
    """
    This is a decorator that is used to store rest api calls
    check https://realpython.com/lru-cache-python/
    :param max_size: The size of the lru cache
    :param time_limit: the time by which the lru cache expires
    :return: cache
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=max_size)(func)

        func.lifetime = timedelta(seconds=time_limit)

        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()

                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


class FetchBlogData:
    def __init__(self, tags: list, sort_by: str = "id", desc: bool = False) -> None:
        """
        Constructor
        :param tags: A list of tags, for each tag in the list a call is made to the API
        :param sort_by: The key by which we sort the results
        :param desc: Sort the final result by ascending or descending order, descending if this is True
        """
        self.url = "https://api.hatchways.io/assessment/blog/posts?tag="
        self.tags = tags
        self.sort_by = sort_by
        self.descending = False
        if desc:
            self.descending = True
        self.__lock = Lock()
        self.__result = []
        self.__id_set = set()

    @timed_lru_cache(128, 3600)
    def __contact_url(self, url) -> requests:
        """
        This method contacts the url and returns a response
        :param url:
        :return:
        """
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def __add_blog_data_to_result(self, url: str) -> None:
        """
        This method adds the response retrieved from a tag to the result list
        :param url: the url (along with the tag) to which we make the ap call
        :return: None
        """
        logger.debug("fetching results for url = {}".format(url))
        try:
            blog_data = self.__contact_url(url)
        except requests.RequestException:
            logger.exception("Exception occurred while contacting url {}".format(url))
            return

        if "posts" in blog_data:
            self.__lock.acquire()
            for entry in blog_data["posts"]:
                # prevent duplicate results from being added to the result, we check the set to see if the id is there.
                if "id" in entry and entry["id"] not in self.__id_set:
                    self.__result.append(entry)
                    self.__id_set.add(entry["id"])
            self.__lock.release()

    def __check_result(self) -> bool:
        """
        This method checks if the final result list is empty
        :return: boolean, if the final result list is none then return False else True
        """
        # check if result is null
        if len(self.__result) == 0:
            return False
        else:
            return True

    def __sort(self, sort_key: str, desc: bool = False) -> list:
        """
        Sort the result according to the key mentioned by the user.
        :param sort_key: key by which the list of dictionaries need to be sorted
        :param desc: if we need to sort by descending (reverse) or ascending
        :return: Sorted list
        """
        return sorted(self.__result, key=lambda x: x[sort_key], reverse=desc)

    def fetch(self) -> list:
        """
        This is the method that creates threads for each tag in the tag list, checks if the result is valid
        and returns the list
        :return: final result list
        """
        # first we check if the url is up
        try:
            test_tag = "tech"
            url = self.url + test_tag
            r = self.__contact_url(url)
        except requests.RequestException:
            logger.exception("Exception raised url {}".format(self.url))
            return ["website down"]

        thread_list = []
        # create threads for each tag
        for tag in self.tags:
            url = self.url + tag
            t = threading.Thread(target=self.__add_blog_data_to_result, args=(url,))
            thread_list.append(t)
        for t in thread_list:
            t.start()
        # wait for threads to complete
        for t in thread_list:
            t.join()

        # if the calls to api does not return any result
        if not self.__check_result():
            return []

        # we then sort the result based on the key provided by the user
        try:
            result = self.__sort(self.sort_by, self.descending)
            return result
        except KeyError:
            # if the user mentions a sort by string that does not exist
            # catch the exception
            logger.exception("Sort by key {} does not exist in the result".format(self.sort_by))
            # sort by default which is "id"
            result = self.__sort("id", self.descending)
            return result


def main():
    test_fetch = FetchBlogData(["tech", "culture", "history"], "popularity", True)
    result = test_fetch.fetch()
    for i in result:
        print(i)


if __name__ == "__main__":
    main()
