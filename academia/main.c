#include <gtk/gtk.h>
#include <stdio.h>

// Variáveis globais
GtkWidget *label;
GtkWidget *progress_bar;
int contador = 1;
guint id_timeout;

// Função para atualizar a label e a barra de progresso
gboolean atualizar_label_e_barra_de_progresso(gpointer data) {
    char texto[50];
    sprintf(texto, "Número: %d", contador);
    gtk_label_set_text(GTK_LABEL(label), texto);
    
    double progresso = (double)contador / 12;
    gtk_progress_bar_set_fraction(GTK_PROGRESS_BAR(progress_bar), progresso);

    if (contador <= 12) {
        contador++;
    } else {
        // Se a contagem atingir 12, interromper o timeout
        g_source_remove(id_timeout);
    }

    return G_SOURCE_CONTINUE;
}

// Função chamada quando o botão "Iniciar" é clicado
void iniciar_contagem(GtkWidget *widget, gpointer data) {
    contador = 1;
    // Reiniciar a barra de progresso
    gtk_progress_bar_set_fraction(GTK_PROGRESS_BAR(progress_bar), 0.0);
    // Iniciar a contagem chamando a função de atualização
    id_timeout = g_timeout_add_seconds(5, atualizar_label_e_barra_de_progresso, NULL);
}

// Função chamada quando o botão "Parar" é clicado
void parar_contagem(GtkWidget *widget, gpointer data) {
    // Interromper apenas o timeout, não encerrar o loop principal do GTK
    if (id_timeout > 0) {
        g_source_remove(id_timeout);
        id_timeout = 0;  // Define como 0 para evitar remoção duplicada
    }
}

// Função chamada quando a janela é redimensionada
void redimensionar_janela(GtkWidget *widget, GdkEvent *event, gpointer data) {
    GtkAllocation allocation;
    gtk_widget_get_allocation(widget, &allocation);
    int largura_widgets = allocation.width * 0.8;

    gtk_widget_set_size_request(label, largura_widgets, -1);
    gtk_widget_set_size_request(progress_bar, largura_widgets, -1);
}

int main(int argc, char *argv[]) {
    // Inicialização do GTK
    gtk_init(&argc, &argv);

    // Criar janela principal
    GtkWidget *janela = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(janela), "Contagem");
    gtk_window_set_default_size(GTK_WINDOW(janela), 300, 200);
    g_signal_connect(janela, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(janela, "size-allocate", G_CALLBACK(redimensionar_janela), NULL);

    // Obtém a tela primária
    GdkDisplay *display = gdk_display_get_default();
    GdkMonitor *monitor = gdk_display_get_primary_monitor(display);

    // Obtém a área de trabalho (workspace) do monitor primário
    GdkRectangle area_trabalho;
    gdk_monitor_get_workarea(monitor, &area_trabalho);

    // Calcula a largura dos widgets como 80% da largura da área de trabalho
    int largura_widgets = area_trabalho.width * 0.8;

    // Criar container de grade
    GtkWidget *grid = gtk_grid_new();
    gtk_grid_set_row_spacing(GTK_GRID(grid), 10);
    gtk_grid_set_column_spacing(GTK_GRID(grid), 10);
    gtk_container_add(GTK_CONTAINER(janela), grid);

    // Criar label para exibir o número
    label = gtk_label_new("Número: 0");
    gtk_widget_set_hexpand(label, TRUE);
    gtk_widget_set_vexpand(label, TRUE);
    gtk_grid_attach(GTK_GRID(grid), label, 0, 0, 2, 1);

    // Criar barra de progresso
    progress_bar = gtk_progress_bar_new();
    gtk_widget_set_hexpand(progress_bar, TRUE);
    gtk_widget_set_vexpand(progress_bar, TRUE);
    gtk_grid_attach(GTK_GRID(grid), progress_bar, 0, 1, 2, 1);

    // Criar botão "Iniciar"
    GtkWidget *botao_iniciar = gtk_button_new_with_label("Iniciar");
    g_signal_connect(botao_iniciar, "clicked", G_CALLBACK(iniciar_contagem), NULL);
    gtk_widget_set_hexpand(botao_iniciar, TRUE);
    gtk_widget_set_vexpand(botao_iniciar, TRUE);
    gtk_grid_attach(GTK_GRID(grid), botao_iniciar, 0, 2, 1, 1);

    // Criar botão "Parar"
    GtkWidget *botao_parar = gtk_button_new_with_label("Parar");
    g_signal_connect(botao_parar, "clicked", G_CALLBACK(parar_contagem), NULL);
    gtk_widget_set_hexpand(botao_parar, TRUE);
    gtk_widget_set_vexpand(botao_parar, TRUE);
    gtk_grid_attach(GTK_GRID(grid), botao_parar, 1, 2, 1, 1);

    // Centralizar a grade na janela
    gtk_widget_set_halign(grid, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(grid, GTK_ALIGN_CENTER);

    // Ajustar a largura dos widgets
    gtk_widget_set_size_request(janela, largura_widgets, -1);

    // Exibir todos os widgets
    gtk_widget_show_all(janela);

    // Iniciar loop principal do GTK
    gtk_main();

    return 0;
}
