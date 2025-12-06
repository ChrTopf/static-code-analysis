using System;
using System.Collections.Generic;
using System.Linq;

namespace CoffeeShopExample
{
    public class CoffeeShop
    {
        private List<string> menu;
        private Dictionary<string, decimal> prices;
        private Queue<string> orderQueue;
        private decimal dailyRevenue;

        public CoffeeShop(string shopName)
        {
            menu = new List<string> { "Espresso", "Latte", "Cappuccino", "Americano", "Mocha" };
            prices = new Dictionary<string, decimal>
            {
                { "Espresso", 2.50m },
                { "Latte", 4.00m },
                { "Cappuccino", 3.75m },
                { "Americano", 3.25m },
                { "Mocha", 4.50m }
            };
            orderQueue = new Queue<string>();
            dailyRevenue = 0;
        }

        public void ProcessOrder(string customerName, string drinkType)
        {
            if (string.IsNullOrEmpty(customerName))
            {
                throw new ArgumentException("Customer name cannot be empty");
            }
            if (!menu.Contains(drinkType))
            {
                throw new ArgumentException($"Drink {drinkType} is not available");
            }
            string order = $"{customerName} - {drinkType}";
            orderQueue.Enqueue(order);
            decimal price = prices[drinkType];
            dailyRevenue += price;
            Console.WriteLine($"Order added: {order} (${price})");
            Console.WriteLine($"Queue length: {orderQueue.Count}");
            Console.WriteLine($"Daily revenue: ${dailyRevenue:F2}");
        }

        public string GenerateDailyReport()
        {
            var report = new System.Text.StringBuilder();
            report.AppendLine("=== DAILY COFFEE SHOP REPORT ===");
            report.AppendLine($"Date: {DateTime.Now:yyyy-MM-dd}");
            report.AppendLine($"Total Revenue: ${dailyRevenue:F2}");
            report.AppendLine($"Orders in Queue: {orderQueue.Count}");
            report.AppendLine();

            if (orderQueue.Count > 0)
            {
                report.AppendLine("Pending Orders:");
                var orders = orderQueue.ToArray();
                for (int i = 0; i < orders.Length; i++)
                {
                    report.AppendLine($"{i + 1}. {orders[i]}");
                }
            }
            else
            {
                report.AppendLine("No pending orders.");
            }

            report.AppendLine();
            report.AppendLine("Menu & Prices:");
            foreach (var item in menu)
            {
                report.AppendLine($"- {item}: ${prices[item]:F2}");
            }

            report.AppendLine();
            var averageOrderValue = orderQueue.Count > 0 ? dailyRevenue / orderQueue.Count : 0;
            report.AppendLine($"Average Order Value: ${averageOrderValue:F2}");

            if (dailyRevenue > 100)
            {
                report.AppendLine("🎉 Great sales day!");
            }
            else if (dailyRevenue > 50)
            {
                report.AppendLine("Good progress today.");
            }
            else
            {
                report.AppendLine("Slow day - consider promotions.");
            }

            return report.ToString();
        }

        public bool IsMenuItemAvailable(string drinkType)
        {
            if (string.IsNullOrWhiteSpace(drinkType))
            {
                return false;
            }
            bool isAvailable = menu.Contains(drinkType);
            if (isAvailable)
            {
                Console.WriteLine($"{drinkType} is available for ${prices[drinkType]:F2}");
            }
            else
            {
                Console.WriteLine($"{drinkType} is not on our menu");
                Console.WriteLine("Available drinks: " + string.Join(", ", menu));
            }
            return isAvailable;
        }
    }
}