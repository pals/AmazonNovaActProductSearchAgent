from nova_act import NovaAct
from pydantic import BaseModel
import json
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

class Product(BaseModel):
    product_name:str
    product_price: float
    where: str
    product_description: str

class ProductsList(BaseModel):
    products: list[Product]

def productSearch(productName: str, website: str) -> Product | None:
    # print(f"productName: {productName}")
    # print(f"website: {website}")

    with NovaAct(
        starting_page="https://google.com/"
    ) as nova:
        nova.act(f"Look for search bar to type search query and enter {productName} ")
        nova.act(f"Check search results. Look for {website} website for {productName} baby product in results. ")
        results = nova.act(f"If you find {website} for {productName} in google search results, open the serach result by clicking on it in same browser tab and get {productName} information. ", schema=Product.model_json_schema())
    
        # print(f"{website} results: {results}")

        if not results.matches_schema:
            # print(f"Invalid JSON {results=}")
            return None
        searchedProduct = Product.model_validate(results.parsed_response)
        searchedProduct.where = website
        # print(f"{results} product result: {searchedProduct}")

        return searchedProduct

def main(product_name):
    # print("This is the main function!")
    all_results: list[Product] = []

    # searchProduct = "newborn huggies diapers"
    website = "Amazon"

    searchResult = productSearch(product_name, website)
    # all_results.extend(searchResult)
    all_results.append(searchResult)

    website = "Walmart"
    searchResult = productSearch(product_name, website)
    # all_results.extend(searchResult)
    all_results.append(searchResult)

    website = "Target"
    searchResult = productSearch(product_name, website)
    # all_results.extend(searchResult)
    all_results.append(searchResult)

    # print(f"Found products: {all_results}")
    # print(json.dumps(all_results))  # Output results as JSON
    # print(all_results) # Output results as JSON
    return all_results
    

        
       

# This condition checks if the script is being run directly
# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        product_name = sys.argv[1]
        search_results = main(product_name)
        # logger.debug(f"JSON output: {json.dumps(search_results)}")

        # print(json.dumps(search_results))  # Output results as JSON
        json_output = json.dumps([product.model_dump() for product in search_results], indent=2)
        print(json_output)

    else:
        print(json.dumps({"error": "Product name not provided to script."}))