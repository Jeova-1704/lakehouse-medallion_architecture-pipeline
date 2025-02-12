from elt.gold.LakehouseConnection import LakehouseConnection


def create_table_analise_clientes_pedido(df_clientes, df_pedidos, df_produtos):
    df_clientes = df_clientes.rename(columns={"id": "id_cliente"})
    df_pedidos = df_pedidos.rename(columns={"id": "id_pedido"})
    df_produtos = df_produtos.rename(columns={"id": "id_produto"})
    
    df_pedidos = df_pedidos.merge(df_produtos[["id_produto", "nome_produto", "categoria"]], on="id_produto", how="left")
    df_agrupado = df_pedidos.groupby("id_cliente").agg(
        total_pedidos=("id_pedido", "count"),
        total_gasto=("valor_total", "sum"),
        data_primeiro_pedido=("data_pedido", "min"),
        data_ultimo_pedido=("data_pedido", "max"),
        categorias_compradas=("categoria", lambda x: ", ".join(set(x.dropna()))),
        produtos_comprados=("nome_produto", lambda x: ", ".join(set(x.dropna())))
    ).reset_index()
    
    df_final = df_agrupado.merge(df_clientes, on="id_cliente", how="left")
    
    df_final = df_final[["id_cliente", "nome", "cidade", "idade", "total_pedidos", "total_gasto", "data_primeiro_pedido", "data_ultimo_pedido", "categorias_compradas", "produtos_comprados"]]
    
    return df_final


def create_analise_produtos(df_pedidos, df_produtos):
    df_pedidos = df_pedidos.rename(columns={"id": "id_pedido"})
    df_produtos = df_produtos.rename(columns={"id": "id_produto"})
    
    df = df_pedidos.groupby("id_produto").agg(
        total_vendido=("quantidade", "sum"),
        total_receita=("valor_total", "sum")
    ).reset_index()

    df = df.merge(df_produtos[["id_produto", "nome_produto", "categoria", "estoque"]], on="id_produto", how="left")

    df.rename(columns={"estoque": "estoque_atual"}, inplace=True)

    return df


def remove_duplicates_cliente_pedido(df, df_gold, column_name):
    df = df.drop_duplicates(subset=[column_name])
    
    if df_gold.empty:
        print(f"A camada Gold está vazia. Inserindo todos os {len(df)} registros.")
        return df
    
    df[column_name] = df[column_name].astype(str)
    df_gold[column_name] = df_gold[column_name].astype(str)
    
    df_final = df[~df[column_name].isin(df_gold[column_name])]
    
    return df_final
    


def main():
    lakehouse = LakehouseConnection()
    data_clientes = lakehouse.get_data_from_lakehouse("clientes", "silver")
    data_produtos = lakehouse.get_data_from_lakehouse("produtos", "silver")
    data_pedidos = lakehouse.get_data_from_lakehouse("pedidos", "silver")
    
    df_analise_clientes_pedido = create_table_analise_clientes_pedido(data_clientes, data_pedidos, data_produtos)
    df_analise_produtos = create_analise_produtos(data_pedidos, data_produtos)
    
    df_analise_clientes_pedido_gold = lakehouse.get_data_from_lakehouse("analise_clientes_pedidos", "gold")
    df_analise_produtos_gold = lakehouse.get_data_from_lakehouse("analise_produtos", "gold")
    
    df_analise_clientes_pedido = remove_duplicates_cliente_pedido(df_analise_clientes_pedido, df_analise_clientes_pedido_gold, "id_cliente")
    df_analise_produtos = remove_duplicates_cliente_pedido(df_analise_produtos, df_analise_produtos_gold, "id_produto")
    
    size_clientes_pedido = df_analise_clientes_pedido.shape[0]
    size_produtos = df_analise_produtos.shape[0]
    
    if size_clientes_pedido == 0 and size_produtos == 0:
        print("Não há dados novos para inserir na camada Gold.")
        lakehouse.close_connection()
        return 
    
    lakehouse.insert_data_to_lakehouse(df_analise_clientes_pedido, "analise_clientes_pedidos", "gold")
    lakehouse.insert_data_to_lakehouse(df_analise_produtos, "analise_produtos", "gold")
    
    lakehouse.close_connection()
    
    
if __name__ == "__main__":
    main()
