# Cuisine classification of recipes based on ingredients

If the HTML is not rendering, click on the following to see the -

Binary classification notebook
https://htmlpreview.github.io/?https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/model_implementation/recipe_binary_classification/recipe%20binary%20classification.html

Multi-classification notebook
https://htmlpreview.github.io/?https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/model_implementation/recipe_multiclass_classification/recipe%20multiclass%20classification.html

My blog post about this project is [published on Towards Data Science](https://towardsdatascience.com/https-towardsdatascience-com-end-to-end-recipe-cuisine-classification-e97f4ac22104 "Recipe Cuisine Classifier Blog post")


<table>
<tbody>
  <tr>
    <th td style="text-align: center;" colspan="8">Model Results</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>
    <td>Count</td>
    <td>260</td>
    <td>387</td>
    <td>787</td>
    <td>2520</td>
    <td>75</td>
    <td>148</td>
  </tr>
    <tr>  
 <th td style="text-align: center;" colspan="8">Multinomial Logistic Regression (MLR)</th>
      </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>

  <tr>
    <td><br>Test F1 score<br></td>
    <td>0.81</td>
    <td>0.58</td>
    <td>0.95</td>
    <td>0.93</td>
    <td>0.69</td>
    <td>0.76</td>
  </tr>
  <tr>
    <td>Train F1 score<br></td>
    <td>1.0</td>
    <td>0.98</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>0.99</td>
    <td>1.0</td>
  </tr>
  <tr>
    <th td style="text-align: center;" colspan="8">Class Weighted Loss Function (MLR)</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>
    <td>Test F1 score</td>
    <td>0.82</td>
    <td>0.65</td>
    <td>0.95</td>
    <td>0.94</td>
    <td>0.79</td>
    <td>0.77</td>
  </tr>
  <tr>
    <td>Train F1 score</td>
    <td>1.0</td>
    <td>0.99</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>1.0</td>
  </tr>
  <tr>
    <th td style="text-align: center;" colspan="8">Undersampling (MLR)</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>
    <td>Test F1 score</td>
    <td>0.68</td>
    <td>0.44</td>
    <td>0.89</td>
    <td>0.77</td>
    <td>0.49</td>
    <td>0.60</td>
  </tr>
  <tr>
    <td>Train F1 score</td>
    <td>0.93</td>
    <td>0.80</td>
    <td>0.91</td>
    <td>0.84</td>
    <td>0.99</td>
    <td>0.92</td>
  </tr>
  <tr>       
    <th td style="text-align: center;" colspan="8">Oversampling (MLR)</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>
    <td>Test F1 score</td>
    <td>0.80</td>
    <td>0.65</td>
    <td>0.94</td>
    <td>0.93</td>
    <td>0.83</td>
    <td>0.75</td>
  </tr>
  <tr>
    <td>Train F1 score</td>
    <td>1.0</td>
    <td>0.98</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>1.0</td>
  </tr>
  <tr>     
    <th td style="text-align: center;" colspan="8">CHI Score (top 600)</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>    
    <td>Test F1 score</td>
    <td>0.76</td>
    <td>0.46</td>
    <td>0.94</td>
    <td>0.91</td>
    <td>0.73</td>
    <td>0.72</td>
  </tr>
  <tr>
    <td>Train F1 score</td>
    <td>0.89</td>
    <td>0.62</td>
    <td>0.96</td>
    <td>0.94</td>
    <td>0.93</td>
    <td>0.93</td>
  </tr>
  <tr>
    <th td style="text-align: center;" colspan="8">Deep Learning w/ Keras - densely connected network</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>
    <td>Test F1 score</td>
    <td>0.71</td>
    <td>0.54</td>
    <td>0.92</td>
    <td>0.94</td>
    <td>0.47</td>
    <td>0.57</td>
  </tr>
  <tr>
    <td>Train F1 score</td>
    <td>0.99</td>
    <td>0.99</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>1.0</td>
    <td>1.0</td>
  </tr>
  <tr>
    <th td style="text-align: center;" colspan="8">Deep Learning w/ Keras - Multichannel n-gram with embedding and Conv1D</th>
  </tr>
  <tr>
    <td>Cuisine</td>
    <td>Chinese</td>
    <td>French</td>
    <td>Indian</td>
    <td>Italian</td>
    <td>Mexican</td>
    <td>Thai</td>
  </tr>
  <tr>
    <td>Test F1 score</td>
    <td>0.72</td>
    <td>0.49</td>
    <td>0.91</td>
    <td>0.97</td>
    <td>0.74</td>
    <td>0.73</td>
  </tr>
  <tr>
    <td>Train F1 score</td>
    <td>0.98</td>
    <td>0.99</td>
    <td>0.99</td>
    <td>0.99</td>
    <td>0.98</td>
    <td>0.98</td>
  </tr>
    </tbody>
</table>

- Class Weighted had top scores for Chinese, French, Indian
- Italian did the best with Conv1D and multigram embedding, followed by Class Weighted.
- Mexican did best with oversampling, followed by Class Weighted.

The overall best model, that I go with for the AWS deployment will be Class weighted loss function.

Other ideas in addition to collecting more data is considering the quantity of an ingredient as part of the feature weight.


