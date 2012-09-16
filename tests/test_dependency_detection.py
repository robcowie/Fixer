# -*- coding: utf-8 -*-

from nose.tools import *
import fixer


def test_no_dependencies():
    """Multiple fixtures with no dependencies
    """

    class A(fixer.Fixture):
        name = u'Foo'

    class B(fixer.Fixture):
        name = u'Anon'

    class C(fixer.Fixture):
        name = u'Ymous'

    fixtures = [A, B, C]

    loader = fixer.Loader(None, None, processor=fixer.DebugProcessor)
    deps_graph = loader.dependencies(fixtures)

    ## All fixtures are in the dependency graph
    assert_items_equal(deps_graph.nodes(), fixtures)

    ## There are 3 dependency graphs (i.e. all 3 nodes are leaf nodes)
    dependency_trees = list( loader.iter_dependency_trees(deps_graph) )
    assert_equal(len(dependency_trees), len(fixtures))



def test_one_level_dependencies():
    """Multiple fixtures with one dependency level
           A
           |
        --- ---
        |     |
        B     C
    """

    class A(fixer.Fixture):
        name = u'Foo'

    class B(fixer.Fixture):
        name = u'Anon'
        friend = A

    class C(fixer.Fixture):
        name = u'Ymous'
        friend = A

    fixtures = [A, B, C]

    loader = fixer.Loader(None, None, processor=fixer.DebugProcessor)
    deps_graph = loader.dependencies(fixtures)

    ## All fixtures are in the dependency graph
    assert_items_equal(deps_graph.nodes(), fixtures)

    ## There is 1 dependency graph starting with A (A --> B, A --> C)
    dependency_trees = list( loader.iter_dependency_trees(deps_graph) )
    assert_equal(len(dependency_trees), 1)

    ## The dependency tree from A contains B and C as nodes
    depend_on_a = dependency_trees[0][1].nodes()
    assert_in(B, depend_on_a)
    assert_in(C, depend_on_a)

    ## TODO: REplace above assertion with test that B and C are adjacent to A in graph


def test_two_level_dependencies():
    """Multiple fixtures with two dependency levels
            A
            |
            B
            |
            C
    """

    class A(fixer.Fixture):
        name = u'Foo'

    class B(fixer.Fixture):
        name = u'Anon'
        friend = A

    class C(fixer.Fixture):
        name = u'Ymous'
        friend = B

    fixtures = [A, B, C]

    loader = fixer.Loader(None, None, processor=fixer.DebugProcessor)
    deps_graph = loader.dependencies(fixtures)

    ## All fixtures are in the dependency graph
    assert_items_equal(deps_graph.nodes(), fixtures)

    ## There is 1 dependency graph starting with A (A --> B --> C)
    dependency_trees = list( loader.iter_dependency_trees(deps_graph) )
    assert_equal(len(dependency_trees), 1)

    ## B is adjacent to A and C is adjacent to B
    tree = dependency_trees[0][1]
    assert_items_equal(tree.edges(), [(A, B), (B, C)])


def test_two_level_branched_dependencies():
    """Multiple fixtures with two dependency levels and branch
           A
           |
        --- ---
        |     |
        B     D
        |
        C
    """

    class A(fixer.Fixture):
        name = u'Foo'

    class B(fixer.Fixture):
        name = u'Anon'
        friend = A

    class C(fixer.Fixture):
        name = u'Ymous'
        friend = B

    class D(fixer.Fixture):
        name = u'Sidamo'
        friend = A

    fixtures = [A, B, C, D]

    loader = fixer.Loader(None, None, processor=fixer.DebugProcessor)
    deps_graph = loader.dependencies(fixtures)

    ## All fixtures are in the dependency graph
    assert_items_equal(deps_graph.nodes(), fixtures)

    ## There is 1 dependency graph starting with A
    dependency_trees = list( loader.iter_dependency_trees(deps_graph) )
    assert_equal(len(dependency_trees), 1)

    ## B is adjacent to A and C is adjacent to B AND D is adjacent to A
    tree = dependency_trees[0][1]
    assert_items_equal(tree.edges(), [(A, B), (B, C), (A, D)])
