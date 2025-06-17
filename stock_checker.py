import requests
import json
import time
import os
from datetime import datetime
import sys

def load_urls_from_file(filename="url.txt"):
    """
    Load URLs from url.txt file - one URL per line
    """
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found!")
        return []
    
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('http'):
                        urls.append(line)
                    else:
                        print(f"⚠️ Line {line_num}: Invalid URL format - {line}")
        
        print(f"✅ Loaded {len(urls)} URLs from {filename}")
        return urls
        
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return []

def extract_product_tag(product_url):
    """
    Extract product tag from Xiaomi URL
    URL format: https://www.mi.co.id/id/product/redmi-13x/?skupanel=1&gid=4223716725
    """
    try:
        if '/product/' not in product_url:
            print('❌ Invalid product URL format')
            return None
            
        # Extract tag between /product/ and /
        url_parts = product_url.split('/product/')
        if len(url_parts) < 2:
            print('❌ Cannot extract product tag from URL')
            return None
            
        tag = url_parts[1].split('/')[0].split('?')[0]
        return tag
        
    except Exception as e:
        print(f'❌ Error extracting product tag: {e}')
        return None

def check_stock_single(product_url, product_index=None):
    """
    Check stock availability once via API
    """
    try:
        # Extract product tag from URL
        tag = extract_product_tag(product_url)
        if not tag:
            return False
            
        # Xiaomi stock API endpoint
        stock_api_url = f"https://go.buy.mi.co.id/id/misc/getgoodsinformation?from=mobile&tag={tag}"
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.mi.co.id',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.mi.co.id/id/product/redmi-13x/',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
        }
        
        prefix = f'[{product_index}] ' if product_index else ''
        print(f'🔍 {prefix}Checking product: {tag}')
        
        response = requests.get(stock_api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                stock_data = response.json()
                
                # Parse JSON directly - access nested structure
                is_cos = str(stock_data['data']['goodsinformation'][0]['is_cos'])
                product_name = stock_data['data']['goodsinformation'][0].get('goods_name', 'Unknown Product')
                
                # Get additional product info
                product_info = stock_data['data']['goodsinformation'][0]
                market_price = product_info.get('market_price', 'N/A')
                sale_price = product_info.get('sale_price', 'N/A')
                
                print(f'📦 {prefix}Product: {product_name}')
                print(f'💰 {prefix}Market Price: {market_price}')
                print(f'💸 {prefix}Sale Price: {sale_price}')
                
                if is_cos == "False":
                    print(f'✅ {prefix}STOCK AVAILABLE! (is_cos: False)')
                    return True
                else:
                    print(f'❌ {prefix}OUT OF STOCK (is_cos: {is_cos})')
                    return False
                
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                print(f'❌ {prefix}JSON parsing error: {str(e)}')
                return False
        else:
            print(f'❌ {prefix}HTTP Error: {response.status_code}')
            return False
            
    except requests.exceptions.RequestException as e:
        print(f'❌ {prefix}Request failed: {str(e)}')
        return False
    except Exception as e:
        print(f'❌ {prefix}Unexpected error: {e}')
        return False

def check_all_urls_once(urls):
    """
    Check stock status for all URLs once
    """
    print('📦 CHECKING ALL PRODUCTS ONCE')
    print('=' * 40)
    
    results = []
    available_products = []
    
    for i, url in enumerate(urls, 1):
        print(f'\n🔍 Product {i}/{len(urls)}:')
        print('-' * 25)
        
        is_available = check_stock_single(url, i)
        
        result = {
            'product_number': i,
            'url': url,
            'available': is_available,
            'checked_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        results.append(result)
        
        if is_available:
            available_products.append(i)
    
    # Summary
    print('\n📊 STOCK CHECK SUMMARY')
    print('=' * 30)
    
    for result in results:
        status = '✅ AVAILABLE' if result['available'] else '❌ OUT OF STOCK'
        print(f"Product {result['product_number']}: {status}")
    
    available_count = len(available_products)
    print(f'\n📈 Available: {available_count}/{len(urls)} products')
    
    if available_products:
        print(f'🎉 Available products: {", ".join(map(str, available_products))}')
    
    # Save results
    filename = f"stock_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'💾 Results saved to: {filename}')
    
    return results

def monitor_all_urls_continuous(urls, check_interval=5):
    """
    Continuously monitor all URLs forever - never stop checking
    """
    print('🔄 CONTINUOUS MONITORING ALL PRODUCTS (NEVER STOP)')
    print('=' * 60)
    print(f'📦 Total products: {len(urls)}')
    print(f'⏰ Check interval: {check_interval} seconds')
    print(f'🚀 Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'🔄 Will keep checking forever until manually stopped (Ctrl+C)')
    print('=' * 60)
    
    check_count = 0
    start_time = datetime.now()
    total_available_found = 0
    
    try:
        while True:  # Forever loop - never break
            check_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            
            print(f'\n📡 Stock Check Round #{check_count} at {current_time}')
            print('=' * 40)
            
            available_products = []
            
            for i, url in enumerate(urls, 1):
                print(f'\n🔍 Product {i}/{len(urls)}:')
                print('-' * 20)
                
                is_available = check_stock_single(url, i)
                
                if is_available:
                    available_products.append(i)
            
            # Show results for this round
            if available_products:
                total_available_found += len(available_products)
                
                print('\n' + '🎉' * 40)
                print('🎉 STOCK AVAILABLE IN THIS ROUND! 🎉')
                print('🎉' * 40)
                print(f'✅ Available products: {", ".join(map(str, available_products))}')
                print(f'📊 Total available products found so far: {total_available_found}')
                print(f'🕐 Found at: {current_time}')
                
                # Save result to file each time we find available stock
                result = {
                    'timestamp': current_time,
                    'round_number': check_count,
                    'available_products_this_round': available_products,
                    'total_products': len(urls),
                    'total_available_found': total_available_found,
                    'monitoring_duration': str(datetime.now() - start_time),
                    'urls': urls
                }
                
                filename = f"stock_found_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f'💾 Result saved to: {filename}')
                
                print('\n🔄 CONTINUING TO MONITOR...')
                print('=' * 40)
            else:
                print(f'\n❌ No products available in this round...')
            
            print(f'⏰ Waiting {check_interval} seconds before next round...')
            print(f'📊 Stats: Round #{check_count} | Available found: {total_available_found} | Running time: {datetime.now() - start_time}')
            time.sleep(check_interval)
                
    except KeyboardInterrupt:
        end_time = datetime.now()
        duration = end_time - start_time
        
        print('\n' + '⏹️ ' * 40)
        print('⏹️  MONITORING STOPPED BY USER (Ctrl+C)')
        print('⏹️ ' * 40)
        print(f'⏱️  Total monitoring time: {duration}')
        print(f'📊 Total check rounds completed: {check_count}')
        print(f'🎯 Total available products found: {total_available_found}')
        
        # Save final summary
        final_result = {
            'session_ended': current_time,
            'total_rounds': check_count,
            'total_monitoring_time': str(duration),
            'total_available_found': total_available_found,
            'stopped_by': 'user_interrupt',
            'urls_monitored': urls
        }
        
        filename = f"monitoring_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(final_result, f, indent=2)
        print(f'💾 Final summary saved to: {filename}')
        print('👋 Goodbye!')
        
    except Exception as e:
        print(f'\n❌ Monitoring error: {e}')
        print('🔄 Will try to continue...')
        time.sleep(5)  # Wait 5 seconds and continue

def main():
    """
    Main function with simple menu
    """
    print('🚀 XIAOMI STOCK CHECKER')
    print('=' * 30)
    
    # Load URLs from file
    urls = load_urls_from_file("url.txt")
    
    if not urls:
        print("❌ No valid URLs found!")
        print("Please create url.txt with one URL per line:")
        print("https://www.mi.co.id/id/product/product1/")
        print("https://www.mi.co.id/id/product/product2/")
        return
    
    print(f"\n📋 Found {len(urls)} products to check:")
    for i, url in enumerate(urls, 1):
        tag = extract_product_tag(url)
        print(f"  {i}. {tag}")
    
    print('\nSelect an option:')
    print('1. Check all products once')
    print('2. Monitor all products continuously')
    print('3. Exit')
    
    try:
        choice = input('\nEnter choice (1-3): ').strip()
        
        if choice == '1':
            print('\n🔍 Checking all products once...')
            check_all_urls_once(urls)
            
        elif choice == '2':
            interval = input('\nCheck interval in seconds (default 5): ').strip()
            interval = int(interval) if interval.isdigit() else 5
            print(f'\n🔄 Starting continuous monitoring (interval: {interval}s)...')
            monitor_all_urls_continuous(urls, interval)
            
        elif choice == '3':
            print('👋 Goodbye!')
            
        else:
            print('❌ Invalid choice!')
            
    except KeyboardInterrupt:
        print('\n👋 Goodbye!')
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    main() 
