package src

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"reaper/src/queue"
	"strings"
	"sync"
)

type Fingerprint struct {
	Fp      string   `json:"fp"`
	Headers []string `json:"headers"`
	Body    []string `json:"body"`
	Icon    []string `json:"icon"`
	JS      []string `json:"js"`
	Title   []string `json:"title"`
	Regexp  string   `json:"regexp"`
}

type Data struct {
	Fingerprints []Fingerprint `json:"fingerprints"`
}

var (
	Buffer      = make(chan string, 2048) // 全局缓冲区
	BufferMutex sync.Mutex                // 用于保护缓冲区的互斥锁
	IsFlush     bool                      // 手动执行flush
	Fps         []Fingerprint             // 指纹数组
	Thread      int                       // 最大线并发数
	Wg          sync.WaitGroup
	UrlQueue    *queue.Queue
)

// var Fps []Fingerprint
// var

func read_json() []Fingerprint {
	// 读取 JSON 文件
	filePath := "reaper.json"

	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return nil
	}
	defer file.Close()

	var data Data
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&data)
	if err != nil {
		fmt.Println("Error parsing JSON:", err)
		return nil
	}

	fps := data.Fingerprints
	return fps
}

func read_url() {
	filePath := "url.txt"
	UrlQueue = queue.NewQueue()
	// maxThreads := Thread
	// semaphore := make(chan struct{}, maxThreads)

	// 打开文件
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error read url.txt:", err)
		return
	}
	defer file.Close()

	// 创建 Scanner 对象
	scanner := bufio.NewScanner(file)

	// 逐行读取文件内容并去除换行符
	for scanner.Scan() {
		url := scanner.Text()
		url = strings.TrimSpace(url)       // 去除每行两端的空白字符
		url = strings.TrimSuffix(url, "/") // 去掉 "/"

		// 判断是否以 "http" 开头，如果不是则添加 "http"
		if !strings.HasPrefix(url, "http") {
			url = "http://" + url
		}

		// urlQueue <- url // 将url加入队列
		UrlQueue.Push(url)

		// Wg.Add(1)
		// semaphore <- struct{}{} // 限制并发的信号量
		// go func(url string) {
		// 	defer func() { <-semaphore }()
		// 	defer Wg.Done()
		// 	All(url)
		// }(url)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error scanner url.txt:", err)
	}

	// Wg.Wait()

}

func sendUrl() {
	defer Wg.Done()
	for UrlQueue.Len() != 0 {
		dataface := UrlQueue.Pop()
		url, _ := dataface.(string)
		// fmt.Println(url)
		All(url)
	}
}

func scan() {
	fmt.Printf("thread: %d", Thread)
	for i := 0; i <= Thread; i++ {
		Wg.Add(1)
		go sendUrl()
	}
	Wg.Wait()
}

func Begin() {
	flag.IntVar(&Thread, "t", 100, "最大并发数, 默认100")
	flag.Parse()
	read_url()
	Fps = read_json()
	filePath := "result.csv"
	// 创建或覆盖文件
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	// 写入字符串到文件
	content := "url,fingerprint,server,status,length,title\n"
	_, err = file.WriteString(content)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	scan()

	defer func() {
		WriteFile()
	}()

	// 处理程序退出信号
	// exitSignal := make(chan os.Signal, 1)
	// signal.Notify(exitSignal, syscall.SIGINT, syscall.SIGTERM)
}
