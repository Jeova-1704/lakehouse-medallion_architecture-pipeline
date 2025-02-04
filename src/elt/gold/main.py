from LakehouseConnection import LakehouseConnection


def create_table_analise_clientes_pedido(df_clientes, df_pedidos, df_produtos):
    df_pedidos = df_pedidos.merge(df_produtos[["id_produto", "nome_produto", "categoria"]], on="id_produto", how="left")
    df_agrupado = df_pedidos.groupby("id_cliente").agg(
        total_pedidos=("id_pedido", "count"),  # Conta o número de pedidos
        total_gasto=("valor_total", "sum"),  # Soma o valor total gasto
        data_primeiro_pedido=("data_pedido", "min"),  # Obtém a data do primeiro pedido
        data_ultimo_pedido=("data_pedido", "max"),  # Obtém a data do último pedido
        categorias_compradas=("categoria", lambda x: ", ".join(set(x.dropna()))),  # Lista única de categorias compradas
        produtos_comprados=("nome_produto", lambda x: ", ".join(set(x.dropna())))  # Lista única de produtos comprados
    ).reset_index()
    
    df_final = df_agrupado.merge(df_clientes, on="id_cliente", how="left")
    
    df_final = df_final[["id_cliente", "nome", "cidade", "idade", "total_pedidos", "total_gasto", "data_primeiro_pedido", "data_ultimo_pedido", "categorias_compradas", "produtos_comprados"]]
    
    return df_final



def create_analise_produtos(df_pedidos, df_produtos):
    df = df_pedidos.groupby("id_produto").agg(
        total_vendido=("quantidade", "sum"),
        total_receita=("valor_total", "sum")
    ).reset_index()

    df = df.merge(df_produtos[["id_produto", "nome_produto", "categoria", "estoque"]], on="id_produto", how="left")

    # Renomeamos colunas para o padrão da tabela Gold
    df.rename(columns={"estoque": "estoque_atual"}, inplace=True)

    return df


def app():
    lakehouse = LakehouseConnection()
    data_clientes = lakehouse.get_data_from_lakehouse("clientes", "silver")
    data_produtos = lakehouse.get_data_from_lakehouse("produtos", "silver")
    data_pedidos = lakehouse.get_data_from_lakehouse("pedidos", "silver")
    
    df_analise_clientes_pedido = create_table_analise_clientes_pedido(data_clientes, data_pedidos, data_produtos)
    # df_analise_produtos = create_analise_produtos(data_pedidos, data_produtos)
    
    print(df_analise_clientes_pedido.shape)
    # print(df_analise_produtos.shape)
    
    lakehouse.insert_data_to_lakehouse(df_analise_clientes_pedido, "analise_clientes_pedidos", "gold")
    # lakehouse.insert_data_to_lakehouse(df_analise_produtos, "analise_produtos", "gold")
    
    lakehouse.close_connection()
    
if __name__ == "__main__":
    app()