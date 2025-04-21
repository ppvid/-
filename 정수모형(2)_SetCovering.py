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