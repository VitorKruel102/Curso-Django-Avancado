from authors.forms.recipe_form import AuthorRecipeForm
from django.http.response import Http404
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe



@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch' 
    # ^ É o método que buscar qo método pedido para a View. Aqui sé não estiver logado, ele nem procura o método
)
class DashboardRecipe(View):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_recipe(self, id=None): 
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)

        self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None, # Precisa ter no form um atributo --> enctype="multipart/form-data"
            instance=recipe
        )

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(                
                reverse(
                    'authors:dashboard_recipe_edit', args=(
                        recipe.id,
                    )
                )
            )

        self.render_recipe(form)