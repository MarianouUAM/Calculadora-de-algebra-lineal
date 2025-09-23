using System;

class OperacionesMatrices
{
    static void Main()
    {
        Console.WriteLine("=== OPERACIONES CON MATRICES ===");
        Console.WriteLine("Por: Tu Nombre");

        bool continuar = true;

        while (continuar)
        {
            MostrarMenu();
            string opcion = Console.ReadLine();

            switch (opcion)
            {
                case "1":
                    SumarMatrices();
                    break;
                case "2":
                    RestarMatrices();
                    break;
                case "3":
                    MultiplicarMatrices();
                    break;
                case "4":
                    continuar = false;
                    Console.WriteLine("¡Hasta luego!");
                    break;
                default:
                    Console.WriteLine("Opción no válida. Intente nuevamente.");
                    break;
            }

            if (continuar)
            {
                Console.WriteLine("\nPresione cualquier tecla para continuar...");
                Console.ReadKey();
                Console.Clear();
            }
        }
    }

    static void MostrarMenu()
    {
        Console.WriteLine("\n=== MENÚ PRINCIPAL ===");
        Console.WriteLine("1. Suma de matrices");
        Console.WriteLine("2. Resta de matrices");
        Console.WriteLine("3. Multiplicación de matrices");
        Console.WriteLine("4. Salir");
        Console.Write("Seleccione una opción (1-4): ");
    }

    static void SumarMatrices()
    {
        Console.WriteLine("\n=== SUMA DE MATRICES ===");

        // Solicitar dimensiones
        Console.Write("Ingrese el número de filas: ");
        int filas = int.Parse(Console.ReadLine());

        Console.Write("Ingrese el número de columnas: ");
        int columnas = int.Parse(Console.ReadLine());

        // Crear matrices
        int[,] matrizA = new int[filas, columnas];
        int[,] matrizB = new int[filas, columnas];
        int[,] resultado = new int[filas, columnas];

        // Ingresar valores
        Console.WriteLine("\n--- MATRIZ A ---");
        IngresarMatriz(matrizA, "A");

        Console.WriteLine("\n--- MATRIZ B ---");
        IngresarMatriz(matrizB, "B");

        // Mostrar matrices originales
        Console.WriteLine("\n--- MATRICES ORIGINALES ---");
        MostrarMatriz(matrizA, "Matriz A");
        MostrarMatriz(matrizB, "Matriz B");

        // Realizar suma paso a paso
        Console.WriteLine("--- PROCESO DE SUMA ---");
        for (int i = 0; i < filas; i++)
        {
            for (int j = 0; j < columnas; j++)
            {
                int valorA = matrizA[i, j];
                int valorB = matrizB[i, j];
                int suma = valorA + valorB;
                resultado[i, j] = suma;

                Console.WriteLine($"A[{i + 1},{j + 1}] + B[{i + 1},{j + 1}] = {valorA} + {valorB} = {suma}");
            }
        }

        // Mostrar resultado
        Console.WriteLine("\n--- RESULTADO: A + B ---");
        MostrarMatriz(resultado, "A + B");
    }

    static void RestarMatrices()
    {
        Console.WriteLine("\n=== RESTA DE MATRICES ===");

        // Solicitar dimensiones
        Console.Write("Ingrese el número de filas: ");
        int filas = int.Parse(Console.ReadLine());

        Console.Write("Ingrese el número de columnas: ");
        int columnas = int.Parse(Console.ReadLine());

        // Crear matrices
        int[,] matrizA = new int[filas, columnas];
        int[,] matrizB = new int[filas, columnas];
        int[,] resultado = new int[filas, columnas];

        // Ingresar valores
        Console.WriteLine("\n--- MATRIZ A ---");
        IngresarMatriz(matrizA, "A");

        Console.WriteLine("\n--- MATRIZ B ---");
        IngresarMatriz(matrizB, "B");

        // Mostrar matrices originales
        Console.WriteLine("\n--- MATRICES ORIGINALES ---");
        MostrarMatriz(matrizA, "Matriz A");
        MostrarMatriz(matrizB, "Matriz B");

        // Realizar resta paso a paso
        Console.WriteLine("--- PROCESO DE RESTA ---");
        for (int i = 0; i < filas; i++)
        {
            for (int j = 0; j < columnas; j++)
            {
                int valorA = matrizA[i, j];
                int valorB = matrizB[i, j];
                int resta = valorA - valorB;
                resultado[i, j] = resta;

                Console.WriteLine($"A[{i + 1},{j + 1}] - B[{i + 1},{j + 1}] = {valorA} - {valorB} = {resta}");
            }
        }

        // Mostrar resultado
        Console.WriteLine("\n--- RESULTADO: A - B ---");
        MostrarMatriz(resultado, "A - B");
    }

    static void MultiplicarMatrices()
    {
        Console.WriteLine("\n=== MULTIPLICACIÓN DE MATRICES ===");

        // Solicitar dimensiones de A
        Console.Write("Ingrese el número de filas de la matriz A: ");
        int filasA = int.Parse(Console.ReadLine());

        Console.Write("Ingrese el número de columnas de la matriz A: ");
        int columnasA = int.Parse(Console.ReadLine());

        // Solicitar dimensiones de B
        Console.Write("Ingrese el número de filas de la matriz B: ");
        int filasB = int.Parse(Console.ReadLine());

        Console.Write("Ingrese el número de columnas de la matriz B: ");
        int columnasB = int.Parse(Console.ReadLine());

        // Validar compatibilidad
        if (columnasA != filasB)
        {
            Console.WriteLine("\n❌ ERROR: No se pueden multiplicar las matrices.");
            Console.WriteLine($"   El número de columnas de A ({columnasA}) debe ser igual al número de filas de B ({filasB})");
            return;
        }

        // Crear matrices
        int[,] matrizA = new int[filasA, columnasA];
        int[,] matrizB = new int[filasB, columnasB];
        int[,] resultado = new int[filasA, columnasB];

        // Ingresar valores
        Console.WriteLine("\n--- MATRIZ A ---");
        IngresarMatriz(matrizA, "A");

        Console.WriteLine("\n--- MATRIZ B ---");
        IngresarMatriz(matrizB, "B");

        // Mostrar matrices originales
        Console.WriteLine("\n--- MATRICES ORIGINALES ---");
        MostrarMatriz(matrizA, "Matriz A");
        MostrarMatriz(matrizB, "Matriz B");

        // Realizar multiplicación paso a paso
        Console.WriteLine("--- PROCESO DE MULTIPLICACIÓN ---");
        for (int i = 0; i < filasA; i++)
        {
            for (int j = 0; j < columnasB; j++)
            {
                Console.WriteLine($"\n📊 Calculando elemento [{i + 1},{j + 1}]:");
                int suma = 0;

                for (int k = 0; k < columnasA; k++)
                {
                    int valorA = matrizA[i, k];
                    int valorB = matrizB[k, j];
                    int producto = valorA * valorB;
                    suma += producto;

                    Console.WriteLine($"  A[{i + 1},{k + 1}] × B[{k + 1},{j + 1}] = {valorA} × {valorB} = {producto}");
                }

                resultado[i, j] = suma;
                Console.WriteLine($"  ✅ Suma total = {suma}");
            }
        }

        // Mostrar resultado
        Console.WriteLine("\n--- RESULTADO: A × B ---");
        MostrarMatriz(resultado, "A × B");
    }

    static void IngresarMatriz(int[,] matriz, string nombre)
    {
        int filas = matriz.GetLength(0);
        int columnas = matriz.GetLength(1);

        Console.WriteLine($"Ingresando valores para la matriz {nombre} ({filas}x{columnas}):");

        for (int i = 0; i < filas; i++)
        {
            for (int j = 0; j < columnas; j++)
            {
                Console.Write($"  {nombre}[{i + 1},{j + 1}]: ");
                matriz[i, j] = int.Parse(Console.ReadLine());
            }
        }
    }

    static void MostrarMatriz(int[,] matriz, string nombre)
    {
        int filas = matriz.GetLength(0);
        int columnas = matriz.GetLength(1);

        Console.WriteLine($"{nombre}:");

        // Encabezado de columnas
        Console.Write("     ");
        for (int j = 0; j < columnas; j++)
        {
            Console.Write($"Col {j + 1}".PadLeft(8));
        }
        Console.WriteLine();

        // Filas con números
        for (int i = 0; i < filas; i++)
        {
            Console.Write($"Fila {i + 1}:");
            for (int j = 0; j < columnas; j++)
            {
                Console.Write($"{matriz[i, j],8}");
            }
            Console.WriteLine();
        }
        Console.WriteLine();
    }
}