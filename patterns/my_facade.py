# a facade brings together disparate entities via a single facade
# remember these classes should be in separate modules
class Employee():
    '''abstract base class'''
    def __init__(self):
        pass

class Coder(Employee):
    '''creates code to solve problems'''
    def __init__(self):
        print('write sme code')
    def __is_available(self): # this is mangled (__)  so it is only visible within instances
        '''we could check if the coder resource is available'''
        print('coding skills are available')
        return True # or False
    def book_time(self):
        if self.__is_available():
            print('coder has been booked')

class Tester(Employee):
    '''tests code to ensure diligence'''
    def __init__(self):
        print('preparing some test')
    def testing(self):
        print('test are in place')

class Technician(Employee):
    def __init__(self):
        print('preparing equipment for the team')
    def doStuff(self):
        print('network, machines, cloud all in place')

class Artisan(Employee):
    '''design stuff'''
    def __init__(self):
        print('designing things')
    def make_prototype(self):
        print('wireframes are ready')

class Manager():
    '''This is a facade to the other classes'''

    employees = [Coder(), Coder(), Tester()]    # list of Employee subclass objects
    projects = ['Project 1']    # list of project name strings
    
    def __init__(self):
        print('Manager says I can arrange the team')
        
    def hire_employee(self, employee_type):
        '''employee_type: one of Coder, Tester, Technician, Artisan'''
        print(f'(Manager) Hired a new employee of type {employee_type}.')
        new_employee = eval(employee_type)()
        self.employees.append(new_employee)
        
    def plan_project(self, project_name, coders_needed=0, testers_needed=0, technicians_needed=0, artisans_needed=0):
        print('\n== Planning Project 1... ==')
        if project_name not in self.projects:
            self.projects += project_name
            print(f'Created new project "{project_name}"')
        else:
            print(f'Using existing project "{project_name}"')

        coder_count, tester_count, technician_count, artisan_count = 0, 0, 0, 0
        for employee in self.employees:
            if isinstance(employee, Coder): coder_count += 1
            if isinstance(employee, Tester): tester_count += 1
            if isinstance(employee, Technician): technician_count += 1
            if isinstance(employee, Artisan): artisan_count += 1
        employee_info_str = f'''Manager says, we currently have:
        {coder_count} coders
        {tester_count} testers
        {technician_count} technicians
        {artisan_count} artisans
        '''
        needed_info_str = f'''The project requires
        {coders_needed} coders
        {testers_needed} testers
        {technicians_needed} technicians
        {artisans_needed} artisans
        '''
  
        coders_to_hire = max(0, coders_needed - coder_count)
        testers_to_hire = max(0, testers_needed - tester_count)
        technicians_to_hire = max(0, technicians_needed - technician_count)
        artisans_to_hire = max(0, artisans_needed - artisan_count)
        
        to_hire_info_str = f'''We need to hire
        {coders_to_hire} new coders
        {testers_to_hire} new testers
        {technicians_to_hire} new technicians
        {artisans_to_hire} new artisans
        '''
        
        print(employee_info_str)
        print(needed_info_str)
        print(to_hire_info_str)
        
        for _ in range(coders_to_hire):
            self.hire_employee('Coder')
        
        for _ in range(testers_to_hire):
            self.hire_employee('Tester')
            
        for _ in range(technicians_to_hire):
            self.hire_employee('Technician')
            
        for _ in range(artisans_to_hire):
            self.hire_employee('Artisan')

        # coders_to_hire * self.hire_employee('Coder')
        # testers_to_hire * self.hire_employee('Tester')
        # technicians_to_hire * self.hire_employee('Technician')
        # artisans_to_hire * self.hire_employee('Artisan')
        
    def execute_project(self, project_name):
        # put the assets to work
        print('\n== Executing Project 1... ==')
        
        for employee in self.employees:
            if isinstance(employee, Coder):
                employee.book_time()
            if isinstance(employee, Tester):
                employee.testing()
            if isinstance(employee, Technician):
                employee.doStuff()
            if isinstance(employee, Artisan):
                employee.make_prototype()
        
    def arrange(self):
        '''The facade will provide instances of all the other subsystems/microservices etc.'''
        self.plan_project('Project 1', coders_needed=4, testers_needed=1, technicians_needed=2, artisans_needed=5)
        self.execute_project('Project 1')
        

class Client():
    '''Client needs resources to solve a problem'''
    def __init__(self):
        print('We need a team for our project')
    def askManager(self):
        print('lets talk to the manager')
        self.manager = Manager() # we now have access to our facade
        self.manager.arrange()
    def __del__(self): # every class will run __del__ whn done
        print('All done')

if __name__ == '__main__':
    '''a facade can make ugly stuff easier to look at'''
    customer = Client()
    customer.askManager()
