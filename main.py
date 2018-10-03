from repositories import CategoriesRespository, EbayApiRepository
from utils import Utils
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-b", "--build", action='store_true')
parser.add_argument("-r", "--render", help="the category Id", type=int)
args = parser.parse_args()


def main(args):
    if args.build:
        print('this may take a while, please wait a little bit.')
        CategoriesRespository.createTableIfNecesary()
        categoriesAsText = EbayApiRepository.getAllCategoriesAsText()
        categoriesList = EbayApiRepository.categoriesXmlToListOfTouples(categoriesAsText)
        CategoriesRespository.insertList(categoriesList)
        print('finished processing')
    elif isinstance(args.render, int):
        givenCategoryId = args.render
        categories = CategoriesRespository.getWithChildren(givenCategoryId)
        forest = Utils.flatToTree(categories)
        htmlTree = Utils.printTreeToHtml(forest[0])
        Utils.printToFile('{}.html'.format(givenCategoryId), htmlTree)
    CategoriesRespository.closeConn()


main(args)
