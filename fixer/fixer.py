# -*- coding: utf-8 -*-

import networkx as nx
from sqlalchemy import orm

__all__ = ['FixtureError', 'Fixture', 'FixtureProcessor', 'DebugProcessor', 'Loader']


class FixtureError(Exception):
    pass


class Fixture(object):

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    @property
    def __model_class__(self):
        return self.__model__ or self.__class__.__name__.split('_', 1)[0]


class FixtureProcessor(object):

    def __init__(self, session):
        self.dbsession = session

    def load(self, f):
        klass = f.__model_class__
        try:
            m = globals()[klass]()
        except KeyError:
            raise FixtureError(u'Cannot find model class {0}'.format(klass))

        for k, v in vars(f).iteritems():
            if k.startswith('__'):
                continue
            setattr(m, k, v)

        self.dbsession.add(m)


class DebugProcessor(FixtureProcessor):

    def load(self, f):
        print('Initialising {0}'.format(f))


class Loader(object):

    def __init__(self, metadata, dbsession=None, processor=FixtureProcessor):
        if metadata and not dbsession:
            dbsession = orm.scoped_session(orm.sessionmaker())
            dbsession.configure(bind=metadata.bind)
        self.dbsession = dbsession
        self.metadata = metadata
        self.processor = processor(self.dbsession)

    def init_db(self, drop=True):
        """Create database tables, optionally droping all first
        """
        if drop:
            self.metadata.drop_all()
        self.metadata.create_all()

    def load(self, fixture_set=None):
        """Process a set of fixtures in dependency-order with the currently
        configured processor
        Default fixture_set is all `Fixture` subclasses
        """
        fixture_set = fixture_set or Fixture.__subclasses__()
        deps = self.dependencies(fixture_set)
        # self.visualise(deps)

        for leaf, deps_tree in self.iter_dependency_trees(deps):
            for fixture in nx.topological_sort_recursive(deps_tree):
                self.processor.load(fixture)

    def iter_dependency_trees(self, dependency_graph):
        """Yield top-level fixtures (fixtures without dependencies) and their
        dependency tree
        """
        ## Start with leaf nodes
        leaves = list(n for n, d in dependency_graph.out_degree_iter() if d == 0)

        ## Reverse the dependency graph so we can traverse trees in the correct direction
        reversed_deps = dependency_graph.reverse()

        for leaf in leaves:
            deps_tree = nx.ego_graph(reversed_deps, leaf, radius=None)
            yield leaf, deps_tree

    def dependencies(self, fixture_set):
        """Build a dependency graph of a given set of fixture subclasses
        """
        G = nx.DiGraph()

        for fixture in fixture_set:
            G.add_node(fixture)
            for k, v in vars(fixture).iteritems():
                if isinstance(v, type) and Fixture in v.__bases__:
                    G.add_edge(fixture, v, relationship_name=k)

        if nx.simple_cycles(G):
            raise FixtureError(u'Circular dependencies are not supported')

        return G

    def visualise(self, deps_graph):
        import subprocess
        import tempfile
        f = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        g = nx.to_agraph(deps_graph)
        g.draw(f, format='png', prog='dot')
        subprocess.call(['open', f.name])



if __name__ == '__main__':
    loader = Loader(None)
    # fixture_set = Fixture.__subclasses__()
    # deps = loader.dependencies(fixture_set)
    # loader.visualise(deps)
    loader.load()
