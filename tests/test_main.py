from knowledge_graph_poc import main

import pytest


def test_main_prints_greeting(capsys):
    main()

    captured = capsys.readouterr()
    assert captured.out == "Hello from knowledge-graph-poc!\n"
    assert captured.err == ""
