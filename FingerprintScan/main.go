package main

import (
	"fmt"
	"reaper/src"
)

func main() {
	src.Begin()
	fmt.Println("finished!")
	fmt.Scanln()
	// test()
}

// func test() {
// 	content := res()
// 	escapedBody := "(<!-- Website designed[\\ and powered]* by [^\\|]+\\|\\| Visit: http:\\/\\/snografx.com\\/ -->)"
// 	match, _ := regexp.MatchString(escapedBody, content)
// 	fmt.Println(match)
// }

// func res() string {
// 	urlstring := "https://woniuxy.com/"
// 	transport := &http.Transport{
// 		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
// 	}

// 	// 创建一个http客户端
// 	client := &http.Client{
// 		Timeout:   5 * time.Second,
// 		Transport: transport,
// 	}

// 	// 构建一个 GET 请求
// 	req, err := http.NewRequest("GET", urlstring, nil)
// 	if err != nil {
// 		return ""
// 	}

// 	parsedURL, err := url.Parse(urlstring)
// 	if err != nil {
// 		fmt.Println("Error parsing URL:", err)
// 		return ""
// 	}

// 	host := parsedURL.Host
// 	cookie := &http.Cookie{
// 		Name:  "rememberMe",
// 		Value: "1",
// 	}
// 	req.AddCookie(cookie)
// 	req.Header.Set("Accept", "*/*;q=0.8")
// 	req.Header.Set("Connection", "close")
// 	req.Header.Set("Host", host)
// 	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13")

// 	// 发送请求并获取响应
// 	resp, err := client.Do(req)
// 	if err != nil {
// 		// fmt.Println("Error send resp:", err)
// 		return ""
// 	}
// 	/*
// 		resp.Body.Close() 来关闭该响应体
// 		defer 关键字用于延迟函数的执行，它会在包含它的函数返回之前执行其后的语句。
// 		在当前函数返回之前（也就是 main() 函数执行完毕之前），无论程序执行过程中是否发生错误，都会执行 resp.Body.Close() 来关闭响应体所占用的资源。
// 	*/
// 	defer resp.Body.Close()

// 	// 读取响应内容
// 	body, err := io.ReadAll(resp.Body)
// 	if err != nil {
// 		// fmt.Println("Error read resp.Body:", err)
// 		return ""
// 	}

// 	/*
// 		获取 Content-Type 头部信息
// 		将 Content-Type 转换为小写
// 	*/
// 	contentType := strings.ToLower(resp.Header.Get("Content-Type"))
// 	contentType = strings.ToLower(contentType)

// 	// 将响应体转换为指定的编码格式
// 	httpBodyEncoding, err := charset.NewReader(bytes.NewReader(body), contentType)
// 	if err != nil {
// 		// fmt.Println("Error httpBodyEncoding:", err)
// 		return ""
// 	}

// 	// 读取转换后的内容
// 	convertedBody, err := io.ReadAll(httpBodyEncoding)
// 	if err != nil {
// 		// fmt.Println("Error convertedBody:", err)
// 		return ""
// 	}
// 	httpBody := string(convertedBody)

// 	return httpBody
// }
