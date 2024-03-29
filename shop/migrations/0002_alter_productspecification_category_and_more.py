# Generated by Django 4.0.2 on 2022-03-05 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecification',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='C_product_secification', to='shop.category'),
        ),
        migrations.AlterField(
            model_name='productspecificationvalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P_product_specificatiob_value', to='shop.product'),
        ),
        migrations.CreateModel(
            name='ProducVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Video', models.FileField(default='video/default.mp4', help_text='Upload a product video', upload_to='video/', verbose_name='Video')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alturnative text', max_length=255, null=True, verbose_name='Alturnative text')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_video', to='shop.product')),
            ],
            options={
                'verbose_name': 'Product video',
                'verbose_name_plural': 'Product video',
            },
        ),
    ]
