from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance

# Register your models here.

class BookInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

    @staticmethod
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    #list_filter = ('status', 'due_back')
    fieldsets = ((None, {'fields': ('book', 'imprint', 'id')}), ('Availability', {'fields': ('status', 'due_back', 'borrower')}),)
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')


# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
