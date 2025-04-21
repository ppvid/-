from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#할당문제(화재 대응 시간 최소화)
data=[[5,12,30,20,15],
      [20,4,15,10,25],
      [15,20,6,15,12],
      [25,15,25,4,10],
      [10,25,15,12,5]
]
avg=[2,1,3,1,3]
x={}
#i:소방서 설치 구역 j:할당 지역
for i in range(5):
    for j in range(5):
        x[i,j]=solver.BoolVar('x[%i,%i]'%(i,j))
#두개의 소방서 제약조건(k out of N)
y={}
for i in range(5):
    y[i]=solver.BoolVar('y[%i]'%i)
M=1000000
for i in range(5):
    solver.Add(sum(x[i,j] for j in range(5))<=M*y[i])
solver.Add(sum(y[i] for i in range(5)) ==2)
#모든 구역 한개의 소방서 할당
for j in range(5):
    solver.Add(sum(x[i,j] for i in range(5))==1)
#목적함수 작성하기
obj=solver.Objective()
for i in range(5):
    for j in range(5):
        obj.SetCoefficient(x[i,j],data[i][j]*avg[j])
obj.SetMinimization()

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(obj.Value())
    for i in range(5):
        for j in range(5):
            if x[i,j].solution_value() !=0:
                print(x[i,j].name(),':',x[i,j].solution_value())
    for i in range(5):
        print(y[i].name(),':',y[i].solution_value())
