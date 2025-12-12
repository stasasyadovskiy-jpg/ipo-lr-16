from flask import Blueprint, render_template, request, send_file
import pandas as pd
import io

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        rate = request.form.get('rate', '92.5')
        if not file or file.filename == '':
            return render_template('index.html', error='Выберите файл для загрузки')
        
        try:
            rate = float(rate)
            df = pd.read_excel(file)
            
            df['Цена в RUB'] = df['Цена в USD'] * rate
            df.loc[df['Наличие'] == 0, 'Цена в RUB'] = 'Нет в наличии'
            df = df.sort_values(by='Цена в USD', ascending=False)
            df['Цена в USD'] = df['Цена в USD'].apply(lambda x: f'{x:,.2f}')
            
            output = io.BytesIO()
            df.to_excel(output, index=False, sheet_name='Прайс-лист')
            output.seek(0)
            return send_file(
                output,
                download_name=f'прайс-лист_RUB_{rate}.xlsx',
                as_attachment=True,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except ValueError:
            return render_template('index.html', error='Введите корректный курс (число)')
        except Exception as e:
            return render_template('index.html', error=f'Ошибка обработки файла: {str(e)}')
    
    return render_template('index.html')