#수송문제
#공급하는 양은 공급 능력을 초과할 수 없음
#공급량은 수요량보다 커야함

#예제1_수송문제
#i: 생산한 달, j:설치한 달
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
x={}
for i in range(4):
    for j in range(4):
        if i<=j:
            x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
limit=[25,35,30,10]
demands=[10,15,25,20]
cost=[1.08,1.11,1.1,1.13]
for i in range(4):
    solver.Add(sum(x[i,j] for j in range(4) if j>=i)<=limit[i])
for j in range(4):
    solver.Add(sum(x[i,j] for i in range(4) if i<=j)>=demands[j])
#목적함수
con=[]
for i in range(4):
    for j in range(4):
        if i<=j:
            con.append((cost[i]+0.015*(j-i))*x[i,j])
solver.Minimize(sum(con))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'Total cost = {solver.Objective().Value():.1f}')
    for i in range(4):
        for j in range(4):
            if i<=j:
                print(x[i,j].name(),':',x[i,j].solution_value())
#위의 코드는 제약 조건들을 부등호로 표현했으나 수송 문제의 표준형은 더미 도착지를 만들어 등호로 제약 조건을 설정하는 것이다
#수송문제 표준형은 공급량=수요량이다. 나중에 더미 변수로 간 값들을 보고 해석이 더 용이해지는 등의 이점이 있다

