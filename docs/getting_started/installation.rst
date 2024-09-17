Installation
=============

``drain-swamp-snippet`` is available at PyPi :pypi_org:`drain-swamp-snippet`,
and can be installed from ``pip`` or source as follows.

.. card::

    .. tabs::

        .. code-tab:: bash From ``pip``

            python -m pip install --upgrade drain-swamp-snippet

        .. code-tab:: bash From source

            git clone https://github.com/msftcangoblowm/drain-swamp-snippet
            cd drain-swamp-snippet
            python -m venv .venv
            . .venv/bin/activate
            python -m pip install --upgrade -r requirements/kit.lock -r requirements/prod.lock
            python -m build
            make install

.. raw:: html

    <div class="white-space-20px"></div>
