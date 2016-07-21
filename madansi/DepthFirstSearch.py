import networkx as nx
from madansi.BlastHit import BlastHit
from madansi.GenePresent import GenePresent

class Error(Exception): pass
class DepthFirstSearch(object):
    """Given a node on the given graph, will check that the gene that it represents is present from the lookup table and considers its neighbours to see if they are also present."""    
    def __init__(self,graphfile,filteredfile):
        self.graphfile = graphfile
        self.filteredfile = filteredfile
    
    def open_graphfile(self):
        """Open the given graph file for searching"""
        try:
            g=nx.Graph(nx.drawing.nx_pydot.read_dot(self.graphfile))
            return g
        except IOError:
            raise Error("Error opening this file")
    
    def find_contig(self, gene):
        """Given a gene will find out the contig that it is in"""
        try:
            with open(self.filteredfile,'r') as f:
                for line in f:
                    l = line.rstrip().split('\t')
                    if l[0] == gene:
                        return l[1]
                f.close()
        except IOError:
            raise IOError("Error opening this file")

    def add_node_attribute(self):
        """Adds node attribute to the graph based on whether the gene is given as present in the lookup table as well as the contig that the gene is in"""    
        g = self.open_graphfile()
        gene_dict = GenePresent.construct_dictionary(self)
        for gene in nx.nodes_iter(g):
            g.node[gene]['Contig'] = self.find_contig(gene)
            if gene_dict[gene]:
                g.node[gene]['present']=1
            else:
                g.node[gene]['present']=0
        return g
            
 #   def choose_starting_node(self):
 #       
 #       g=self.add_node_attribute()
 #       for gene in nx.nodes_iter(g):
 #           if g.node[gene]['present']:
 #               start_gene = gene
 #               break
 #       return start_gene
    
    def depth_first_search(self):
        """Modification to the networkx function dfs_edges to search the graph whilst considering whether the vertices """
        g = self.add_node_attribute()
        
        h = g.subgraph([gene for gene in g.nodes() if g.node[gene]['present']])
        
        
        nodes=h
        visited=set()
        list_dfs=[]
        for start in nodes:
            if start in visited:
                continue
            visited.add(start)
            stack = [(start,iter(h[start]))]
            while stack:
                parent,children = stack[-1]
                try:
                    child = next(children)
                    if child not in visited:
                        list_dfs.append((parent,child))
                        visited.add(child)
                        stack.append((child,iter(h[child])))
                except StopIteration:
                    stack.pop()
        return list_dfs
                
    def remove_added_edge_node_attributes(self):
        """Removes the edge attribute 'present' created by the function 'add_node_attribute'"""
        g = self.open_graphfile()
        for gene in nx.nodes_iter(g):
            del g.node[gene]['present']
            
            
        
            
            