import xlrd
from sklearn.feature_extraction.text import CountVectorizer
from core.neuralNet.neural_network import load_neural_network_model, generate_neural_network_model, create_and_save_neural_network


def assignment_of_tasks(text):
    rb = xlrd.open_workbook('core/neuralNet/Выгрузка_студентов.xlsx')
    sheet = rb.sheet_by_index(0)
    all_sentences   = set()   # все заявки (предложения) + названия предприятий + заявитель; сейчас это иксики
    all_groups      = set()   # все рабочие группы

    # читаем всё из экселя в переменные выше
    for rownum in range(1, sheet.nrows):
        row = sheet.row_values(rownum)
        work_group = str(row[9])
        enterprise = str(row[6])
        request_description = str(row[8])
        personal = str(row[5])
        all_sentences.add(request_description)
        all_sentences.add(enterprise)
        all_sentences.add(personal)
        all_groups.add(work_group)

    # со списками удобнее работать (больше методов), поэтому преобразовываю множества в списки
    all_sentences = list(all_sentences)
    all_groups = list(all_groups)

    # сортирую группы, так как при каждом перезапуске кода (при переформировании словаря с группами), он всегда ставит элементы в рандомном порядке.
    # И когда я загружаю нейронку из файла, то индексы групп меняются и пиздец :'(
    all_groups.sort()

    # для примера вывожу
    #print(all_sentences)
    #print(all_groups)

    # создаем векторизатор, чтобы мы могли преобразовывать описания заявок в векторы
    vectorizer = CountVectorizer()
    vectorizer.fit(all_sentences) # используем данные (описание+предприятие+ke_названия) из заявок для формирования векторизатора
    word_count = len(vectorizer.get_feature_names()) # количество элементов в векторе (во входах)

    #для примера: векторизируем предложение и выводим вектор
    x = vectorizer.transform([text]).toarray()
    #print(x)


    # формируем упорядоченные наборы входных и выходных данных
    X = []
    Y = []

    #на случай, если одна заявка занимает более одной строки (идет в несколько раб групп). Это самый пиздецовый момент в коде
    start_index = 1 # строка, от которой начинается одна заявка
    end_index = 1   # строка, в которой заканчивается заявка

    #так как я использую ссылку на предыдущей элемент и мне не нужны заголовки, то начинаю со 2ой строки пробегать по всем строкам
    for rownum in range(2, sheet.nrows):
        row = sheet.row_values(rownum)
        prev_row = sheet.row_values(rownum-1)

        # получаю ид текущей заявки
        id = str(row[2]) or str(row[4]) # получаю id заявки в виде строки...
        id = int(float(id)) # а теперь в виде числа :))

        #id предыдущей заявки
        prev_id = str(prev_row[2]) or str(prev_row[4])  # получаю id предыдущей заявки в виде строки...
        prev_id = int(float(prev_id)) # а теперь в виде числа :))

        # если текущая заяка не является предыдущей или это последняя заявка, то предыдущую (или последнюю) заявку добавляем в датасет...
        if prev_id != id or rownum == sheet.nrows-1:
            work_group = str(prev_row[9])
            enterprise = str(prev_row[6])
            request_description = str(prev_row[8])
            personal = str(prev_row[5])

            # входной вектор - это описание заявки + предприятие + заявитель
            text = request_description + ' ' + enterprise + ' ' + personal
            x = ( vectorizer.transform([text]).toarray()[0].tolist() )
            y = []

            # создаю выходной вектор, заполненный ноликами
            y = [0 for i in range(len(all_groups))]

            # заполняю единички у тех групп, к которым относится заявка
            for i in range(start_index, end_index+1):
                row = sheet.row_values(rownum)
                group_index = all_groups.index(work_group)
                y[group_index] = 1

            #if rownum < 20:
            #    print('work_group ' + work_group + '; ' + request_description)
            X.append(x)
            Y.append(y)
            start_index = rownum
            end_index = rownum
        else:
            end_index = rownum  # иначе прибавляем 1 к индексу строки, в которой заканчивается заявка и ничего не добавляем в датасет


    # обучаю нейронку и сохраняю (подробнее: нажми ctrl+ЛКМ на методе create_and_save_neural_network)
    #model = create_and_save_neural_network(X=X, Y=Y, input_count = word_count, output_count = len(all_groups), epochs=200)

    # загружаю нейронку из файла (подробнее: нажми ctrl+ЛКМ на методе load_neural_network_model)
    model = load_neural_network_model(input_count = word_count, output_count = len(all_groups))


    # тест нейронки
    # формирую вектор входной
    x = vectorizer.transform(['Установка/настройка дополнительного ПО Каримова Оксана Александровна' ]).toarray()

    # формирую выходной вектор
    predict_vector = model.predict([ x ] )[0].tolist()

    # выводу те элементы, которые больше порога 0.3
    result = []
    for index, group in enumerate(predict_vector):
        if group > 0.3:
            #print(    all_groups[index]     )
            result.append(all_groups[index])

    return result



    #print(predict_vector)
    #print(max(predict_vector))
    #print(all_groups[predict_vector.index(max(predict_vector))] )
