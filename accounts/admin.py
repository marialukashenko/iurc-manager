from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db import connection
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def database_manager(request):
    tables = []
    query_results = None
    current_query = ""
    
    # Получаем список всех таблиц
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [{'name': row[0], 'type': row[1]} for row in cursor.fetchall()]
    
    # Выполняем SQL запрос
    if request.method == 'POST' and 'query' in request.POST:
        current_query = request.POST['query']
        try:
            with connection.cursor() as cursor:
                cursor.execute(current_query)
                
                if current_query.strip().lower().startswith('select'):
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    query_results = {
                        'columns': columns,
                        'rows': rows,
                        'row_count': len(rows)
                    }
                else:
                    query_results = {
                        'message': f'Запрос выполнен. Затронуто строк: {cursor.rowcount}',
                        'type': 'OTHER'
                    }
        except Exception as e:
            query_results = {'error': str(e)}
    
    context = {
        **admin.site.each_context(request),
        'title': 'Database Manager',
        'tables': tables,
        'query_results': query_results,
        'current_query': current_query,
    }
    return render(request, 'admin/database_manager.html', context)

original_get_urls = admin.site.get_urls

def custom_get_urls():
    return [
        path('database-manager/', database_manager, name='database_manager'),
    ] + original_get_urls()

admin.site.get_urls = custom_get_urls