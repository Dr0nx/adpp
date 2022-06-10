from datetime import date

from components.unit_of_work import UnitOfWork
from components.cbv import CreateView, ListView
from components.decorators import AppRoute, debug
from components.models import Engine, MapperRegistry
from dr0n_framework.templator import render

site = Engine()
routes = dict()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


# Класс-контроллер - Главная страница
@AppRoute(routes=routes, url='/')
class Index(ListView):
    queryset = site.categories
    template_name = 'index.html'

    # @debug
    # def dispatch(self, *args, **kwargs):
    #     # any custom dispatch code, or just...
    #     super().dispatch(*args, **kwargs)


@AppRoute(routes=routes, url='/contacts/')
class About(ListView):
    template_name = 'contacts.html'


# Класс-контроллер - Страница "Расписания"
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# Класс-контроллер - Страница 404
class NotFound404:
    def __call__(self, request):
        return '404', '404 page not found'


# Класс-контроллер - Страница "Список курсов"
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:

    @debug
    def __call__(self, request):
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# Класс-контроллер - Страница "Создать курс"
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @debug
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(
                    int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# Класс-контроллер - Страница "Создать категорию"
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:

    @debug
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# Класс-контроллер - Страница "Список категорий"
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:

    @debug
    def __call__(self, request):
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# Класс-контроллер - Страница "Список студентов"
@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    @debug
    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


# Класс-контроллер - Страница "Создать студента"
@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    @debug
    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


# Класс-контроллер - Страница "Добавить студента на курс"
@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    @debug
    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    @debug
    def create_obj(self, data):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
