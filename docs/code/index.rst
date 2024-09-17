Code manual
============

.. Apache 2.0 https://github.com/google/material-design-icons
.. Browse Google Material Symbol icons https://fonts.google.com/icons
.. colors https://sphinx-design.readthedocs.io/en/latest/css_classes.html#colors

.. grid:: 2
   :margin: 3
   :padding: 2
   :gutter: 3 3 3 3

   .. grid-item-card:: :material-twotone:`pinch;2em;sd-text-primary` Techniques
      :class-card: sd-border-0

      - :doc:`Snip <snip>`

   .. grid-item-card:: :material-twotone:`foundation;2em;sd-text-muted` Core
      :class-card: sd-border-0

      - :doc:`Constants <general/constants>`
      - :doc:`Check type <general/check_type>`

.. module:: drain_swamp_snippet
   :platform: Unix
   :synopsis: package level exports

    .. py:data:: drain_swamp.__all__
       :type: tuple[str, str, str]
       :value: __all__ = ("ReplaceResult", "Snip", "package_name")

       Package level exports are limited to just custom exceptions. This was originally
       done to avoid unexpected side effects
