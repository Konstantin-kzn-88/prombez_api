import random
from itertools import cycle as iter_cycle

l1 = [1, 2, 3]
# using list iterable as an argument in itertools.cycle()
l2 = iter_cycle(l1)
print(l2)  # Output:<itertools.cycle object at 0x02F794E8>

count = 0
for i in range(1,15):
    print(random.randint(1,3))


if __name__ == '__main__':
    pass
    # with Session(bind=engine) as session:
    #     users = session.query(Users).all()
    #     for user in users:
    #         print(f"{user.id} {user.email} ({user.organizations})")
    #
    #     print('_' * 30)
    #     orgs = session.query(Organizations).all()
    #     for org in orgs:
    #         print(f"{org.id} {org.name_organization} (user_id = {org.user_id})")
    #     print('_' * 30)
    #     objs = session.query(Objects).all()
    #     for obj in objs:
    #         print(f"{obj.id} {obj.name_object} (organization_id = {obj.organization_id})")
    #     print('_' * 30)

    # with Session(bind=engine) as session:
    #     # получаем пользователя user с id==1
    #     t = session.query(Project).filter(Project.id == 2).first()
    #     # удаляем
    #     session.delete(t)
    #     session.commit()
