# Product Generator V2 (11ty-aligned)

This tool ingests a product ZIP (product.md + images/) and produces:
- `src/_data/products/{slug}.yml` (single file with `en:` and `de:` blocks)
- Images copied to `src/assets/images/product/{slug}/`
- Updates `src/_data/products.yml` catalog (adds a card that links to `/{lang}/products/{slug}/`)

## Usage

```bash
python product-generator-v2/processor_v2.py product-generator-v2/inbox/my-product.zip
```

Environment:
- Requires `OPENAI_API_KEY` in environment (or via `.env`)

Input ZIP structure:
```
my-product.zip
├─ product.md
└─ images/
   ├─ product-1.jpg
   └─ ...
```

The LLM parses `product.md` into the internal schema, then we map it to the YAML structure used by pages.


