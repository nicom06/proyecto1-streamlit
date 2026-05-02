import streamlit as st
import numpy as np

st.sidebar.markdown("**Home**")
st.sidebar.title("Proyecto 1 - Aplicacion en Streamlit")

st.sidebar.image("logodmc.png",width=100)

st.sidebar.subheader("Modulo 1 - Python Fundamentals")
st.sidebar.markdown("**Nicole Valeria Mendo Gutierrez**")
st.sidebar.write("Analista de Datos, con el grado de Bachiller en Economía por la Universidad Nacional Federico Villarreal")
st.sidebar.write("2026")
st.sidebar.markdown("""
    Aplicación interactiva desarrollada con **Streamlit** y **Python**
    que integra cuatro módulos funcionales:

    - **Flujo de Caja** — registro y análisis de movimientos financieros  
    - **Registro de Productos** — carga de productos en arrays y DataFrame  
    - **Punto de Equilibrio** — cálculo farmacéutico con librería externa  
    - **Inventario CRUD** — gestión completa de medicamentos  
    """)

#EJERCICIO 1
st.title("1. Flujo de Caja")
st.write("El siguiente formulario nos permite registrar los ingresos y gastos en la tabla de movimientos y nos entrega el balance final")

if "movimientos" not in st.session_state:
    st.session_state.movimientos = []

with st.form("nuevo_movimiento"):
    st.subheader("Registrar Movimiento")
    concepto = st.text_input("Concepto")
    valor = st.number_input("Valor",min_value=1,step=1)
    tipo = st.selectbox("Movimiento",["ingreso","gasto"])
    
    agregar = st.form_submit_button("Agregar Movimiento")

if agregar:
    nuevo = {
        "Concepto":concepto,
        "Valor":valor,
        "Tipo":tipo
    }
    st.session_state.movimientos.append(nuevo)
    st.success(f"Movimiento '{concepto}' agregado correctamente")

if st.session_state.movimientos:
    st.subheader("Tabla de Movimientos")
    st.dataframe(st.session_state.movimientos, use_container_width=True)

total_ingresos = sum(x["Valor"] for x in st.session_state.movimientos if x["Tipo"] == "ingreso")
total_gastos = sum(x["Valor"] for x in st.session_state.movimientos if x["Tipo"] =="gasto")
saldo_final = total_ingresos - total_gastos

st.subheader("Resumen")
col_ingreso, col_gasto, col_saldo = st.columns(3)

with col_ingreso:
    st.metric("Total Ingresos:", f"${total_ingresos}")
with col_gasto:
    st.metric("Total Gastos:", f"${total_gastos}")
with col_saldo:
    st.metric("Saldo Final:", f"${saldo_final}")

st.subheader("Estado del saldo final")
if saldo_final > 0:
    st.success(f"Saldo a FAVOR ${saldo_final}")
elif saldo_final < 0:
    st.error(f"Saldo en CONTRA ${saldo_final}")
else:
    st.warning(f"Saldo en CERO, sin ganacia ni pérdida")


#EJERCICIO 2

import streamlit as st
import pandas as pd
import numpy as np

st.title("2. Registro de producto - Formulario con arrays")

st.markdown("""Esta aplicación permite registrar información en **arrays separados**, los cuales se convierten en un **DataFrame en pandas** que se actualiza cada vez que se agrega un nuevo registro""")

if "nombre_producto" not in st.session_state:
    st.session_state.nombre_producto = []
if "categoria" not in st.session_state:
    st.session_state.categoria = []
if "precio" not in st.session_state:
    st.session_state.precio = []
if "cantidad" not in st.session_state:
    st.session_state.cantidad = []
if "totales" not in st.session_state:
    st.session_state.totales = []

st.subheader("Registro de Producto")

nombre = st.text_input("Nombre de Producto")
categoria = st.selectbox("Categoría",["Antiinfecciosos","Hematologicos","Anestesicos","Salud de la Piel","Salud Renal","Salud Cardiovascular","Neurociencias"])
precio = st.number_input("Precio",min_value=0.0,step=1.0)
cantidad = st.number_input("Cantidad",min_value=1,step=1)

total = precio*cantidad
st.markdown(f"**Total: ${total:.2f}**")

if st.button("Agregar Producto"):
    
    if nombre == "":
        st.error("El nombre del producto no puede estar vacío.")
    else:
        st.session_state.nombre_producto.append(nombre)
        st.session_state.categoria.append(categoria)
        st.session_state.precio.append(precio)
        st.session_state.cantidad.append(cantidad)
        st.session_state.totales.append(total)

        st.success(f"Producto '{nombre}' agregado correctamente.")

#Convertir listas a arrays y luego a Dataframe.
if st.session_state.nombre_producto:
    st.subheader("Tabla de Productos Registrados")

    arreglo_nombre=np.array(st.session_state.nombre_producto)
    arreglo_categoria=np.array(st.session_state.categoria)
    arreglo_precio=np.array(st.session_state.precio)
    arreglo_cantidad=np.array(st.session_state.cantidad)
    arreglo_totales=np.array(st.session_state.totales)

    df=pd.DataFrame({
        "Producto":arreglo_nombre,
        "Categoría":arreglo_categoria,
        "Precio": arreglo_precio,
        "Cantidad":arreglo_cantidad,
        "Total":arreglo_totales
    })

    st.dataframe(df,use_container_width=True)

    st.subheader("Resumen")
    st.markdown(f"- **Total de productos registrados:** {len(arreglo_nombre)}")
    st.markdown(f"- **Suma total de ventas:** ${np.sum(arreglo_totales):.2f}")
    st.markdown(f"- **Precio promedio:** ${np.mean(arreglo_precio):.2f}")
    st.markdown(f"- **Producto más caro:** ${np.max(arreglo_precio):.2f}")
    st.markdown(f"- **Producto más barato:** ${np.min(arreglo_precio):.2f}")
else:
    st.markdown("*Aún no hay productos registrados*")

# EJERCICIO 3
import streamlit as st
import pandas as pd
import numpy as np
from libreria_funciones_proyecto1 import calcular_punto_equilibrio

st.title("3. Punto de Equilibrio")

st.markdown("""
**¿Para qué sirve?**
Calcula la cantidad mínima de unidades de un **medicamento o producto farmacéutico** que se deben vender para cubrir todos los costos, usando la fórmula:

**Punto de Equilibrio = Costos Fijos / (Precio Unitario - Costo Variable Unitario)**
""")

#listas vacías
if "hist_producto" not in st.session_state:
    st.session_state.hist_producto = []
    st.session_state.hist_cf = []
    st.session_state.hist_precio = []
    st.session_state.hist_cv = []
    st.session_state.hist_margen = []
    st.session_state.hist_unidades = []
    st.session_state.hist_ventas = []

#Formulario
st.subheader("Ingresar parámetros")

producto        = st.text_input("Nombre del Medicamento / Producto")
costos_fijos    = st.number_input("Costos Fijos ($)", min_value=0.01, step=100.0)
precio_unitario = st.number_input("Precio de Venta por Unidad ($)", min_value=0.01, step=0.50)
costo_variable  = st.number_input("Costo Variable por Unidad ($)", min_value=0.0, step=0.50)

#Botón
if st.button("Calcular Punto de Equilibrio"):

    if producto == "":
        st.error("Ingresa el nombre del medicamento o producto.")
    else:
        try:
            resultado = calcular_punto_equilibrio(costos_fijos, precio_unitario, costo_variable)

            margen = resultado["margen_contribucion_unitario"]
            unidades = resultado["punto_equilibrio_unidades"]
            ventas = resultado["punto_equilibrio_ventas"]

            # Mostrar resultados
            st.success(f"Resultado para **{producto}**:")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Margen por Unidad", f"${margen}")
            with col2:
                st.metric("Unidades Mínimas", f"{unidades}")
            with col3:
                st.metric("Ventas Mínimas", f"${ventas}")

            #Guardar en listas
            st.session_state.hist_producto.append(producto)
            st.session_state.hist_cf.append(costos_fijos)
            st.session_state.hist_precio.append(precio_unitario)
            st.session_state.hist_cv.append(costo_variable)
            st.session_state.hist_margen.append(margen)
            st.session_state.hist_unidades.append(unidades)
            st.session_state.hist_ventas.append(ventas)

        except ValueError as e:
            st.error(f"Error: {e}")

#Convertir listas a arrays NumPy y mostrar DataFrame
if st.session_state.hist_producto:

    st.subheader("Historial de Cálculos")

    arr_producto  = np.array(st.session_state.hist_producto)
    arr_cf        = np.array(st.session_state.hist_cf)
    arr_precio    = np.array(st.session_state.hist_precio)
    arr_cv        = np.array(st.session_state.hist_cv)
    arr_margen    = np.array(st.session_state.hist_margen)
    arr_unidades  = np.array(st.session_state.hist_unidades)
    arr_ventas    = np.array(st.session_state.hist_ventas)

    df = pd.DataFrame({
        "Producto"         : arr_producto,
        "Costos Fijos"     : arr_cf,
        "Precio Unitario"  : arr_precio,
        "Costo Variable"   : arr_cv,
        "Margen Unitario"  : arr_margen,
        "Unidades Mínimas" : arr_unidades,
        "Ventas Mínimas"   : arr_ventas
    })

    st.dataframe(df, use_container_width=True)

    #Resumen con operaciones NumPy
    st.subheader("Resumen")
    st.markdown(f"- **Productos analizados:** {len(arr_producto)}")
    st.markdown(f"- **Promedio de unidades mínimas:** {np.mean(arr_unidades):.2f} unidades")
    st.markdown(f"- **Producto con mayor punto de equilibrio:** {arr_producto[np.argmax(arr_unidades)]} ({np.max(arr_unidades):.2f} unidades)")
    st.markdown(f"- **Producto con menor punto de equilibrio:** {arr_producto[np.argmin(arr_unidades)]} ({np.min(arr_unidades):.2f} unidades)")

else:
    st.markdown("*Aún no hay registros.*")

#EJERCICIO 4
import streamlit as st
import pandas as pd
from libreria_clases_proyecto1 import InventarioProducto

st.title("4. Inventario")
st.markdown("""Gestión de inventario de **medicamentos y productos farmacéuticos** usando la clase 'InventarioProducto'. Permite registrar, visualizar, actualizar y eliminar los productos del inventarios.""")

if "inventario" not in st.session_state:
    st.session_state.inventario={}

tab_crear,tab_leer,tab_actualizar,tab_eliminar = st.tabs(["Crear","Leer","Actualizar","Eliminar"])

#CREAR
with tab_crear:
    st.subheader("Registrar Nuevo Producto")

    nombre=st.text_input("Nombre Producto",key="c_nombre")
    costo_unitario=st.number_input("Costo unitario",min_value=0.01,step=0.5,key="c_costo")
    precio_unitario=st.number_input("Precio de Venta ($)", min_value=0.01, step=0.50, key="c_precio")
    stock_actual=st.number_input("Stock Actual (unidades)", min_value=0, step=1, key="c_stock")
    stock_minimo=st.number_input("Stock Mínimo (unidades)",min_value=0, step=1,key="c_stock_min")

    if st.button("Agregar Producto",key="btn_crear"):
        if nombre=="":
            st.error("El nombre no puede estar vacío")
        elif nombre in st.session_state.inventario:
            st.error(f"El producto '{nombre}' ya existe. Usa la pestaña Actualizar.")
        else:
            try:
                producto=InventarioProducto(nombre,costo_unitario,precio_unitario,stock_actual,stock_minimo)
                st.session_state.inventario[nombre]=producto
                st.success(f"Producto '{nombre}' agregado correctamente.")
            except ValueError as e:
                st.error(f"Error: {e}")

#LEER
with tab_leer:
    st.subheader("Inventario Actual")

    if not st.session_state.inventario:
        st.info("No hay productos registrados aún.")
    else:
        registros=[p.resumen() for p in st.session_state.inventario.values()]
        df=pd.DataFrame(registros)
        st.columns=["Producto","Stock Actual","Valor Inventario ($)","Margen unitario ($)","Margen (%)", "Necesita Reposición"]
        st.dataframe(df,use_container_width=True)

        #Alerta de reposición
        necesitan=[n for n, p in st.session_state.inventario.items() if p.necesita_reposicion()]
        if necesitan:
            st.warning(f"Productos con stock bajo: **{', '.join(necesitan)}**")
        else:
            st.success("Todos los productos tienen stock suficiente.")

#ACTUALIZAR
with tab_actualizar:
    st.subheader("Actualizar Producto Existente")

    if not st.session_state.inventario:
        st.info("No hay productos por actualizar")
    else:
        nombre_sel=st.selectbox("Selecciona el producto", list(st.session_state.inventario.keys()),key="u_sel")
        p=st.session_state.inventario[nombre_sel]

        st.markdown("**Valores actuales -> modifica los que necesites:**")

        nuevo_costo=st.number_input("Costo Unitarios ($)",value=p.costo_unitario,step=0.5,key="u_costo")
        nuevo_precio=st.number_input("Precio de Venta ($)",value=p.precio_unitario,step=0.5,key="u_precio")
        nuevo_stock=st.number_input("Stock Actual",value=p.stock_actual,step=1,key="u_stock")
        nuevo_min=st.number_input("Stock Mínimo",value=p.stock_minimo,step=1,key="u_min")

        if st.button("Guardar cambios",key="btn_actualizar"):
            try:
                st.session_state.inventarios[nombre_sel]=InventarioProducto(
                    nombre_sel,nuevo_costo,nuevo_precio,nuevo_stock,nuevo_min
                )
                st.success(f"Producto '{nombre_sel}' actualizado correctamente.")
            except ValueError as e:
                st.error(f"Error: {e}")
    
#ELIMINAR
with tab_eliminar:
    st.subheader("Eliminar Prtoducto")

    if not st.session_state.inventario:
        st.info("No hay productos por eliminar.")
    else:
        nombre_del=st.selectbox("Selecciona el producto a eliminar",list(st.session_state.inventario.keys()),key="d_sel")

        if st.button("Eliminar Producto",key="btn_eliminar"):
            del st.session_state.inventario[nombre_del]
            st.success(f"Producto '{nombre_del}' eliminado correctamente.")
            st.rerun()