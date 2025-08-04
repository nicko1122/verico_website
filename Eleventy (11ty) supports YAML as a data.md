Eleventy (11ty) supports YAML as a data format for templates and global data. Here's a quick guide to using YAML in 11ty:

1. Enable YAML Support

By default, 11ty supports YAML for data files. You can use .yaml or .yml extensions for your data files. If you need to explicitly configure YAML support, you can add it in your .eleventy.js configuration file:

Copy code
const yaml = require("js-yaml");

module.exports = function(eleventyConfig) {
  eleventyConfig.addDataExtension("yaml", contents => yaml.load(contents));
  eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));
};

2. Using YAML for Data Files

You can create YAML files in the _data directory to define global or template-specific data. For example:

_data/site.yaml

Copy code
title: My Awesome Site
description: A blog about awesome things.
author:
  name: Jane Doe
  email: jane@example.com


You can then access this data in your templates using the site object:

Copy code
<h1>{{ site.title }}</h1>
<p>{{ site.description }}</p>
<p>Author: {{ site.author.name }}</p>

3. Front Matter in YAML

You can also use YAML for front matter in your content files. For example:

post.md

Copy code
---
title: My First Post
date: 2025-08-03
tags:
  - blog
  - personal
---
This is the content of my first post.

4. Customizing YAML Parsing

If you need advanced YAML parsing or additional features, you can use libraries like js-yaml (as shown above) to customize how YAML files are processed.

This flexibility makes YAML a great choice for managing structured data in your 11ty projects!