import heapq

grid=[

    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]


moves=[(1,0),(-1,0),(0,1),(0,-1)]
#left,rgt,north,south

def heuristic(a,b):
    return 2*(abs(a[0]-b[0]))+ abs(a[1]-b[1])

def astar(start,goal):

    pq=[(0,0,start,[start])]
    visited=set()

    while pq:
        f,g,current,path=heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current==goal:
            return path,g
        
        x,y=current
        for dx,dy in moves:
            nx,ny=x+dx,y+dy
            if 0<nx<len(grid) and 0<=ny<len(grid[0]) and grid[nx][ny]==0:
                new_g=g+2
                h=heuristic((nx,ny),goal)
                new_f=new_g+h
                heapq.heappush(pq,(new_f,new_g,(nx,ny),path+[(nx,ny)]))
    return None,float("inf")

start=(0,0)
goal=(4,4)
path,cost=astar(start,goal)

print("path:",path)
print("total cost:",cost)

