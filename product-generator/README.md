# Product Generator Automation

This tool automates the process of adding new products to the Verico Eleventy website.

## How it works

1.  A `.zip` file containing a new product's information (a `product.md` file and images) is placed in the `inbox` directory.
2.  The `watcher.py` script detects the new file.
3.  It unzips the file into a temporary directory.
4.  It reads the `product.md` file and sends its content to an LLM (OpenAI) for parsing and translation into structured English and German YAML data.
5.  It moves the images to the correct `static/assets/images/product/` directory.
6.  It creates the `en.yml` and `de.yml` data files in the correct `src/_data/content/products/details/` directory.
7.  It updates the `en.yml` and `de.yml` catalog files in `src/_data/content/products/catalog/`.
8.  It creates the `index.njk` page files for both English and German under `src/en/products/` and `src/de/products/`.
9.  The source `.zip` file is deleted from the `inbox`.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    -   Copy `.env.example` to a new file named `.env`.
    -   Add your OpenAI API key to the `.env` file.
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

## Usage

1.  **Run the watcher:**
    ```bash
    python product-generator/watcher.py
    ```

2.  **Add a product:**
    -   Create a `product.md` file following the standard template.
    -   Create an `images` folder containing all product images.
    -   Zip the `product.md` file and the `images` folder. The zip file name should be the product slug (e.g., `my-new-product.zip`).
    -   Drop the `.zip` file into the `product-generator/inbox` directory.

The script will automatically process the file and update the website.


