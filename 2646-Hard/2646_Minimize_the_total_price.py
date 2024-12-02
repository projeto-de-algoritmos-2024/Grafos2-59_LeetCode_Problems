from collections import defaultdict


class Solution(object):
    def minimumTotalPrice(self, n, edges, price, trips):
        """
        :type n: int
        :type edges: List[List[int]]
        :type price: List[int]
        :type trips: List[List[int]]
        :rtype: int
        """
        graph = defaultdict(set)
        
        # make graph
        for n1, n2 in edges:
            graph[n1].add(n2)
            graph[n2].add(n1)

        # find all paths for trips
        paths = []
        for start, end in trips:
            seen = {start}
            q = deque([(start, [])])
            
            while q:
                cur, cur_path = q.popleft()
                cur_path.append(cur)
                if cur == end:
                    paths.append(cur_path)
                    break
                
                for node in graph[cur]:
                    if node not in seen:
                        q.append((node, cur_path[:]))
                        seen.add(node)
        
        # count the number of times nodes are travelled
        nodes_travel_count = defaultdict(int)
        for path in paths:
            for node in path:
                nodes_travel_count[node] += 1

        # dfs to find min cost
        memo = {}
        def find_min_cost(node, parent, can_reduce):
            if (node, parent, can_reduce) in memo:
                return memo[(node, parent, can_reduce)]
            node_count = nodes_travel_count[node]
            
            if can_reduce:
                cost = (price[node] // 2) * node_count
            else:
                cost = price[node] * node_count
            
            
            for child in graph[node]:
                if child == parent:
                    continue
                child_cost = 0
                if can_reduce:
                    child_cost = find_min_cost(child, node, not can_reduce)
                else:
                    child_cost = min(find_min_cost(child, node, True), find_min_cost(child, node, False))
                cost += child_cost
            
            memo[(node, parent, can_reduce)] = cost
            return cost
        
        return min(find_min_cost(0, -1, True), find_min_cost(0, -1, False))
            
        