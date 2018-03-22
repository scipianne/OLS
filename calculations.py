# coding: utf-8

import math


class Matrix(list):
    """
    Список, который считает себя квадратной матрицей
    с шириной int(sqrt(len - 1)) + 1
    """
    def __len__(self):  # переопределяем функцию len как ширину матрицы
        length = super(Matrix, self).__len__()
        if length:
            width = int(math.sqrt(length - 1)) + 1
        else:
            width = 0

        return width

    def __getitem__(self, key):
        width = len(self)
        x, y = key

        return super(Matrix, self).__getitem__(x * width + y)

    def __setitem__(self, key, item):
        width = len(self)
        x, y = key

        return super(Matrix, self).__setitem__(x * width + y, item)


def solve(matr, rez):
    """
    по квадратной матрице n*n matr и n-мерному вектору rez возвращает
    вектор sol, из которого получается исходный домножением на матрицу
    matr * sol = rez
    (решает систему линейных уравнений методом гаусса)
    """
    n = len(matr)
    for i in xrange(n - 1):
        j = i
        while j < n and matr[j, i] == 0:  # находим строку с ненулевым i-тым элементом
            j += 1
        if j != n:
            matr_i = []
            for k in xrange(n):
                matr[j, k], matr[i, k] = matr[i, k], matr[j, k]  # ставим найденную строку на i-тое место
                matr_i.append(matr[i, k])
            rez[j], rez[i] = rez[i], rez[j]
            for k in xrange(i + 1, n):      # вычитаем найденную строку из всех, домножив на коэффициент, чтобы обнулить
                c = matr[k, i] / matr_i[i]  # i-тый столбец всюду, кроме нее
                for l in xrange(n):
                    matr[k, l] -= c * matr_i[l]
                rez[k] -= c * rez[i]
    sol = []
    for i in xrange(n - 1, -1, -1):  # решаем верхнетреугольную систему уравнений
        if matr[i, i]:  # проверка на обратимость матрицы, если на диагонали есть ноль, то решение неоднозначно
            sol_i = rez[i] / matr[i, i]
            sol.append(sol_i)
            for j in xrange(i):
                rez[j] -= matr[j, i] * sol_i
        else:
            return False
    sol.reverse()
    return sol


def find_vct(x, y, n):
    """
    по набору точек x_i и значениям в них y_i строит
    n-мерный вектор - правую часть системы уравнений
    """
    m = len(x)
    vct = []
    for i in xrange(n - 1, -1, -1):
        vct.append(y[0] * x[0] ** i)
    for i in xrange(1, m):
        for j in xrange(n - 1, -1, -1):
            vct[n - j - 1] += y[i] * x[i] ** j
    return vct


def matrix_create(x, n):
    """
    создает матрицу - коэффициенты системы линейных уравнений,
    которую необходимо решить
    """
    m = len(x)
    matr = Matrix()
    for i in xrange(n):
        for j in xrange(n):
            matr.append(1. * x[0] ** (2 * (n - 1) - i - j))
    for k in xrange(1, m):
        for i in xrange(n):
            for j in xrange(n):
                matr[i, j] += 1. * x[k] ** (2 * (n - 1) - i - j)
    return matr


def quad_dif(x, y, a):
    """
    для найденных коэффициентов f(x) считает сумму квадратов
    (y - f(x))^2 согласно мнк
    """
    m = len(x)
    rez = 0
    n = len(a)
    for i in xrange(m):
        square = y[i]
        for j in xrange(n):
            square -= a[j] * (x[i] ** (n - j - 1))
        rez += square ** 2
    return rez


def coef(x, y, deg):
    """
    по набору точек x_i, значений в них y_i и
    желаемой степени deg находит коэффициенты многочлена
    f(x)
    """
    difs = {}
    if deg != 1:  # если задана степень многочлена, пытаемся решить задачу для нее
        matrix = matrix_create(x, deg)
        coef_ = solve(matrix, find_vct(x, y, deg))
        if coef_:
            return coef_
    deg = len(x)  # если степень не задана, берем количество точек как максимум
    for n in xrange(2, deg + 1):      # решаем задачу для всех степеней до выбранного максимума, из решений выбираем
        matrix = matrix_create(x, n)  # оптимальное
        coef_ = solve(matrix, find_vct(x, y, deg))
        if coef_:
            dif = quad_dif(x, y, coef_)
            difs[dif] = coef_
    if difs:
        min_dif = min(difs.keys())
        return difs[min_dif]
    return False
