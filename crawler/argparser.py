import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '--seeds',
    metavar='seeds',
    type=str,
    nargs='+',
    default=None,
    help='keywords & urls to crawl after training')

parser.add_argument(
    '--blacklist_domains',
    metavar='blacklist_domains',
    type=str,
    nargs='+',
    default=None,
    help='domains to ignore when crawling')

parser.add_argument(
    '--relevant_urls',
    metavar='relevant_urls',
    type=str,
    nargs='+',
    default=None,
    required=True,
    help='classifier training')

parser.add_argument(
    '--irrelevant_urls',
    metavar='irrelevant_urls',
    type=str,
    nargs='+',
    default=None,
    required=True,
    help='classifier training')

parser.add_argument(
    '--relevancy_threshold',
    metavar='relevancy_threshold',
    type=float,
    default=0.4,
    help='relevancy threshold for classification')

parser.add_argument(
    '--irrelevancy_threshold',
    metavar='irrelevancy_threshold',
    type=float,
    default=0.2,
    help='relevancy threshold for classification')

parser.add_argument(
    '--page_limit',
    metavar='page_limit',
    type=int,
    default=20,
    help='the number of pages to stop crawling after')

parser.add_argument(
    '--link_limit',
    metavar='link_limit',
    type=int,
    default=10,
    help='the number of links to stop crawling a page after')

parser.add_argument(
    '--adaptive',
    metavar='adaptive',
    type=bool,
    default=False,
    help='continuous learning')

parser.add_argument(
    '--classifier',
    metavar='classifier',
    type=str,
    default="NB",
    help='continuous learning')

parser.add_argument(
    '--vsm',
    metavar='vsm',
    type=bool,
    default=False,
    help='Use VSM model?')

parser.add_argument(
    '--vsm_filter',
    metavar='vsm_filter',
    type=str,
    default="",
    help='vsm_filter model')

parser.add_argument(
    '--min_repo_doc_num',
    metavar='min_repo_doc_num',
    type=int,
    default=5,
    help='')


args = parser.parse_args()
argdict = vars(args)
