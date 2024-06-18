import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
from ResultAnalysisVisualizer import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ResultAnalysisVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Analysis Visualizer")
        
        self.filepath = None
        self.data = None
        self.visualizer = None
        self.home_team = None
        self.away_team = None
        self.teams = set()  # 用来存储所有队伍名称
        
        # 创建一个框架来放置状态栏和按钮
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        # 定义按钮宽度
        button_width = 20
        
        # 创建文件选择按钮
        self.file_button = tk.Button(self.button_frame, text="选择文件", command=self.load_file, width=button_width)
        self.file_button.grid(row=0, column=0, padx=5)
        
        # 创建图片保存按钮
        self.picture_save_button = tk.Button(self.button_frame, text="保存图片文件", command=self.save_picture,state=tk.DISABLED, width=button_width)
        self.picture_save_button.grid(row=0, column=1, padx=5)
        
        # 创建选择主客队按钮
        self.select_home_button = tk.Button(self.button_frame, text="选择主队", command=self.select_home_team, state=tk.DISABLED, width=button_width)
        self.select_home_button.grid(row=0, column=2, padx=5)
        
        self.select_away_button = tk.Button(self.button_frame, text="选择客队", command=self.select_away_team, state=tk.DISABLED, width=button_width)
        self.select_away_button.grid(row=0, column=3, padx=5)
        
        # 创建数据可视化各个按钮
        self.win_rate_button = tk.Button(self.button_frame, text="胜率图", command=self.win_rate_chart, state=tk.DISABLED, width=button_width)
        self.win_rate_button.grid(row=1, column=0, padx=5)
        
        self.score_distribution_button = tk.Button(self.button_frame, text="得分分布图", command=self.score_distribution_chart, state=tk.DISABLED, width=button_width)
        self.score_distribution_button.grid(row=1, column=1, padx=5)
        
        self.diff_goal_frequency_button = tk.Button(self.button_frame, text="得分差距频次图", command=self.diff_goal_histogram, state=tk.DISABLED, width=button_width)
        self.diff_goal_frequency_button.grid(row=1, column=2, padx=5)
        
        self.score_frequency_button = tk.Button(self.button_frame, text="得分频次图", command=self.score_frequency_chart, state=tk.DISABLED, width=button_width)
        self.score_frequency_button.grid(row=1, column=3, padx=5)
        
        # 创建一个画布用于显示图表
        self.canvas_frame = tk.Frame(root,width=640,height=480)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建底部状态栏,显示当前主队和客队
        self.status_bar = tk.Label(root, text="当前主队：None  客队：None", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定关闭窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("txt files", "*.txt")])
        if self.filepath:
            # 读取文件内容，并转换为DataFrame，为其添加列名
            self.data = pd.read_csv(self.filepath, delimiter='\t', header=None, names=['Match', 'Score', 'Details'])
            self.visualizer = ResultAnalysisVisualizer(self.data)
            messagebox.showinfo("文件已加载", f"已选择文件: {self.filepath}")
            self.enable_buttons()
        self.status_bar.config(text=f"当前文件：{self.filepath}")
        
    def enable_buttons(self):
        self.picture_save_button.config(state=tk.NORMAL)
        self.select_home_button.config(state=tk.NORMAL)
        self.select_away_button.config(state=tk.NORMAL)
        self.win_rate_button.config(state=tk.NORMAL)
        self.score_distribution_button.config(state=tk.NORMAL)
        self.diff_goal_frequency_button.config(state=tk.NORMAL)
        self.score_frequency_button.config(state=tk.NORMAL)
        
    def display_plot(self):
    # 清空画布内容
        for widget in self.canvas_frame.winfo_children():
            widget.pack_forget()
        fig = plt.gcf()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def on_closing(self):
        plt.close("all")  # 关闭之前打开的图形窗口，否则容易出现内存警告
        self.root.destroy()
    
    def save_picture(self):
        fig = plt.gcf()
        ax = fig.gca()
        # 设置整个图片的标题
        suptitle = fig._suptitle.get_text() if fig._suptitle else ""
        title = suptitle if suptitle else (ax.get_title() if ax.get_title() else "plot")
        file_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=title, filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

        if file_path:
            fig.savefig(file_path)
            print(f"图片已保存至 {file_path}")
            
    def select_home_team(self):
        self.home_team = simpledialog.askstring("输入", "请输入主队名称：",initialvalue="YuShan2024")
        self.update_status_bar()

    def select_away_team(self):
        self.away_team = simpledialog.askstring("输入", "请输入客队名称：")
        self.update_status_bar()

    def update_status_bar(self):
        self.status_bar.config(text=f"当前主队：{self.home_team}  客队：{self.away_team}")

    def win_rate_chart(self):
        plt.close("all")
        self.visualizer.WinRateChart(self.home_team, self.away_team)
        self.display_plot()

    def score_distribution_chart(self):
        plt.close("all")
        self.visualizer.ScoreDistributionChart(self.home_team, self.away_team)
        self.display_plot()

    def diff_goal_histogram(self):
        plt.close("all")
        self.visualizer.DiffGoalFrequencyChart(self.home_team, self.away_team)
        self.display_plot()

    def score_frequency_chart(self):
        plt.close("all")
        self.visualizer.ScoreFrequencyChart(self.home_team, self.away_team)
        self.display_plot()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ResultAnalysisVisualizerApp(root)
    root.mainloop()