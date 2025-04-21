from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#예제 1
sa = [
 [1, 0, 0, 1, 0, 0],
 [0, 1, 1, 0, 0, 0],
 [0, 1, 0, 0, 0, 1],
 [1, 0, 0, 0, 0, 1],
 [0, 0, 0, 1, 0, 1],
 [0, 0, 1, 0, 0, 0],
 [0, 1, 1, 0, 1, 0],
 [1, 0, 0, 0, 1, 0]
]
costs=[50,40,60,47.5,55,30,57.5,57.2]

x={}
for i in range(8):
    x[i]=solver.BoolVar(f'x[{i}]')
#모든 지역 커버
for j in range(6):
    solver.Add(sum(sa[i][j]*x[i] for i in range(8))>=1)
#목적함수 정의
solver.Minimize(sum(costs[i]*x[i] for i in range(8)))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'{solver.Objective().Value():.1f}')
    for i in range(8):
        if x[i].solution_value()!=0:
            print(x[i].name(),':',x[i].solution_value())
           
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#예제2_interval, 해당값 설정부터
limits = [
 [3500, 3655], [3520, 3905], [3600, 3658], [3650, 4075], [3660, 3915],
 [3900, 4449], [3910, 4095], [3950, 4160], [3995, 4065], [4000, 4195],
 [4000, 4200], [4210, 4405], [4320, 4451], [4350, 4500], [4420, 5400],
 [4450, 4800], [4450, 4570], [5200, 6000], [5600, 6200], [6010, 6400],
 [6015, 6250]
 ]
names = ['PBD', 'PPO', 'PPF', 'PBO', 'PPD', 'POPOP', 'A-NPO', 'NASAL', 'AMINOB', 'BBO', 'D-STILB', 
'D-POPOP', 'A-NOPON', 'D-ANTH',  '4-METHYL-V', '7-D-4-M', 'ESCULIN', 'NA-FLUOR', 
'RHODAMINE-6G', 'RHODAMINE-B', 'ACRIDINE-RED']
costs = [4, 3, 1, 4, 1, 6, 2, 3, 1, 2, 
2, 2, 2, 2, 9, 3, 1, 9, 8, 8, 
2]
#범위 설정
min_v=min(limits[i][0] for i in range(len(limits)))
max_v=max(limits[i][1] for i in range(len(limits)))
#해당하는 값 분리하기
contain={}
for i in range(min_v,max_v+1):
    con=[]
    for j in range(len(limits)):
        if limits[j][0]<=i and limits[j][1]>=i:
            con.append(j)
    contain[i]=con
#구간 나누기
interval=[min_v]
for i in range(min_v,max_v):
    if contain[i]!=contain[i+1]:
        interval.append(i)
interval.append(max_v)
#구간 정의하기
group={}
for i in range(len(interval)-1):
    group[i]=[interval[i],interval[i+1]]
#의사결정변수
x={}
for i in range(len(limits)):
        x[i]=solver.BoolVar(names[i])
#제약조건
for j in group.values():
    solver.Add(sum(x[i] for i in contain[j[0]])>=1)
#목적함수
solver.Minimize(sum(costs[i]*x[i] for i in range(len(limits))))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('Total cost =',solver.Objective().Value())
    for i in range(len(limits)):
         if x[i].solution_value()==1:
             print(x[i].name(),':',x[i].solution_value())
    
