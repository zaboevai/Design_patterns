from fabric.store import MoscowPizzaStore, SaintPetersburgPizzaStore

if __name__ == '__main__':
    moscow_store = MoscowPizzaStore()

    moscow_store.order(moscow_store.menu.cheese_pizza)
    print('------------')
    moscow_store.order(moscow_store.menu.italian_cheese_pizza)
    print('------------')

    piter_store = SaintPetersburgPizzaStore()

    piter_store.order(piter_store.menu.cheese_pizza)
    print('------------')
