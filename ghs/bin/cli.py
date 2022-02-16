#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fire

import ghs.client


def main() -> None:
    """Main function."""
    fire.Fire(ghs.client)


if __name__ == "__main__":
    main()
