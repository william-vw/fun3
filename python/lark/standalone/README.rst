Standalone example
==================

Generate JSON data:
https://json-generator.com/

To initialize, cd to this folder, and run:

.. code-block:: bash

   ./create_standalone.sh

Or:

.. code-block:: bash

   python -m lark.tools.standalone json.lark > json_parser.py

Then run using:

.. code-block:: bash

   python json_parser_main.py <path-to.json>
